import re
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, date
from time import sleep
from sys import exit
from getpass import getpass

br = webdriver.Chrome()

def asynch_access(func):
  hard_fails = 0
  while hard_fails < 1000:
    try:
      return func()
    except NoSuchElementException:
      hard_fails += 1
  raise RuntimeError("Failed to access ")

get_xpath = lambda xpath: br.execute_script('return document.evaluate(\'%s\',document,null,9,null).singleNodeValue' % xpath)

base_addr = "https://courseworks.columbia.edu/portal"
to_absolute_url = lambda stub: "".join((base_addr, stub))
course_addr = to_absolute_url("/site/COMSW3134_001_2014_1")
assignment_frame_addr = to_absolute_url("/tool/1bc627b5-e1d8-4838-a0d7-09ad7465b293?panel=Main")
expand_addr_template = to_absolute_url("/tool/1bc627b5-e1d8-4838-a0d7-09ad7465b293?studentId=%s&panel=Main&sakai_action=doShow_student_submission")


# Logs in to courseworks. If already logged in, has side effect of modifying
# current url of browser
def authenticate():
  login_addr = "/".join((base_addr,"login"))
  br.get(login_addr)
  authenticating = "cas.columbia.edu" in br.current_url
  if not authenticating:
    return
  while True:
    uname = br.find_element_by_id("username")
    pword = br.find_element_by_id("password")
    submit = br.find_element_by_class_name("btn-submit")
    uname.send_keys("ms4249")
    pword.send_keys(getpass())
    submit.click()
    sleep(1)
    try:
      msg = br.find_element_by_id("msg").text
      print msg
      continue
    except NoSuchElementException:
      break

# Requires: Portal
# Navigates to assignment iframe manually
def to_frame_long():
  br.get(course_addr)
  # Space after class name is intentional
  get_btn = lambda: br.find_element_by_class_name("icon-sakai-assignment-grades ")
  assignments_btn = asynch_access(get_btn)
  assignments_btn.click()

  get_iframe = lambda: br.find_element_by_class_name("portletMainIframe")
  iframe = asynch_access(get_iframe)
  frame_link = iframe.get_attribute("src")
  br.get(frame_link)

# Requires: None
# Navigates directly to assignment iframe
def to_frame_short():
  br.get(assignment_frame_addr)

# Requires: Assignment Iframe
# Navigates to List View
def to_list_view():
  get_view = lambda: br.find_element_by_id("view")
  view_select = asynch_access(get_view)
  allOptions = view_select.find_elements_by_tag_name("option")
  # This is the list view option
  allOptions[1].click()

# Requires: Assignment Iframe
# Populates or updates the cache of CW mappings of students to CW_IDs
def cache_cw_ids():
  expand_link_xpath_template = '/html/body/div/form/table/tbody/tr[%d]/td[1]/h4/a'
  name_field_xpath_template = '/html/body/div/form/table/tbody/tr[%d]/td[1]/h4'
  table_xpath = '/html/body/div/form/table'
  id_regex = r'studentId=(.+?)&panel=Main'
  num_students = len(get_xpath(table_xpath).find_elements_by_tag_name("tr")) - 1
  with open("cw_student_ids.txt", "w") as f:
    # Just needs to be bigger than class size
    for i in xrange(2, num_students + 2):
      student_iden = get_xpath(name_field_xpath_template % i).text.strip()
      uni = student_iden.split("(")[-1].strip(")")
      expand_link = get_xpath(expand_link_xpath_template % i).get_attribute("onclick")
      id_ = re.findall(id_regex, expand_link)[0]
      line = " ".join((uni, id_))
      f.write(line)
      # If not the last iteration, advance a line
      if i != (num_students + 1):
        f.write('\n')


def get_cached_cw_ids():
  lines = open("cw_student_ids.txt", "r").read().splitlines()
  uni_to_ids = map(str.split, lines)
  return uni_to_ids

# Requires: None
# Takes the coursework ids and generates expand links from a template
def get_expand_links(ids):
  expand_links = []
  for uni, cw_id in ids:
    link = expand_addr_template % cw_id
    pair = (uni, link)
    expand_links.append(pair)
  return expand_links

# Requires: List View?
# Clicks all expand links and expands student rows
def do_expands(expand_links):
  for uni, link in expand_links:
    br.get(link)
 
# Requires: None
# Takes list of the form ((uni,data),(uni,data),...) as well as first and last
# unis. The returned subset of lst begins with (first_uni,data) and ends with
# (last_uni,data)
def get_uni_data_range(first_uni, last_uni, lst):
  add = False
  range_ = []
  for uni, uni_data in lst:
    if uni == first_uni:
      add = True
    if add:
      range_.append((uni, uni_data))
    if uni == last_uni:
      break
  return range_

# Requires: None
# Takes list of all unis and gets first and last unis from user. The first and
# last unis, inclusive, form the bounds of a subset list of all unis.
def get_bounding_unis(unis):
  while True:
    first_uni = raw_input("Enter First UNI: ")
    if first_uni not in unis:
      print "Invalid UNI"
    else:
      break
  while True:
    last_uni = raw_input("Enter Last UNI: ")
    if last_uni not in unis:
      print "Invalid UNI"
    elif unis.index(last_uni) > unis.index(first_uni):
      print "Last UNI appears before First UNI"
    else:
      break
  return first_uni, last_uni

# Requires: Authentication, List View, Expanded Student Rows
# Returns list of links to student hw pages with the name hw_name
def get_visible_hw_links(hw_name):
  get_all_links = lambda: br.find_elements_by_tag_name("a")
  hrefs = asynch_access(get_all_links)
  hw_hrefs = filter(lambda href: href.text == hw_name, hrefs)
  hw_links = map(lambda href: href.get_attribute("href"), hw_hrefs)
  return hw_links

# Requires: Authentication
# Takes a (uni, hw_link) list and returns a (uni, sub_link) list where sub_link
# is the link (if one exists) to the student submission. sub_link is None if no
# link was found
def get_submission_links(hw_links):
  link_regex = "\"(https.+?attachment/COMSW3134_001_2014_1.+?)\""
  submission_links = []
  for uni, link in hw_links:
    br.get(link)
    sub_links = re.findall(link_regex, br.page_source)
    
    submission_links.append((uni, sub_links))
  return submission_links

def get_cached_hw_links(hw_num):
  fname = "hw%d_links.txt" % hw_num
  return map(str.split, open(fname).read().splitlines())


# VERY SLOW
def get_all_hw_links(hw_name):
  authenticate()
  to_frame_short()
  to_list_view()
  ids = get_cached_cw_ids()
  uni_lst = [pair[0] for pair in ids]
  expand_links = get_expand_links(ids)
  do_expands(expand_links)
  hw_link_lst = get_visible_hw_links(hw_name)
  if len(hw_link_lst) != len(uni_lst):
    print "Number of links retrieved did not match number of unis requested"
    return None
  hw_links = zip(uni_lst, hw_link_lst)
  return hw_links

# Much preferred means of accessing uni range hw links. Can use cached hw
# links, as well.
def get_uni_range_hw_links(hw_num, use_cached_hw_links=True):
  hw_name = "Homework %d" % hw_num
  authenticate()
  ids = get_cached_cw_ids()
  uni_lst = [pair[0] for pair in ids]
  first_uni, last_uni = get_bounding_unis(uni_lst)
  if use_cached_hw_links:
    hw_links = get_cached_hw_links(hw_num)
    hw_links_subset = get_uni_data_range(first_uni, last_uni, hw_links)
  else:
    to_frame_short()
    to_list_view()
    uni_lst_subset = uni_lst[unis.index(first_uni): unis.index(last_uni) + 1]
    expand_links = get_expand_links(ids)
    expand_links_subset = get_uni_data_range(first_uni, last_uni, expand_links)
    do_expands(expand_links_subset)
    hw_link_lst = get_visible_hw_links(hw_name)
    if len(hw_link_lst) != len(uni_lst_subset):
      print "Number of links retrieved did not match number of unis requested"
      return None
    hw_links_subset = zip(uni_lst_subset, hw_link_lst)
  return hw_links_subset

def dump_hw_links(hw_num):
  hw_name = "Homework %d" % hw_num
  fname = "hw%d_links.txt" % hw_num
  with open(fname, "w") as f:
    pairwise_join = lambda pair: " ".join(pair)
    block = "\n".join(map(pairwise_join, get_all_hw_links(hw_name)))
    f.write(block)

def get_all_submission_links(hw_num):
  authenticate()
  return get_submission_links(get_cached_hw_links(hw_num))

authenticate()

to_frame_short()
to_list_view()
print get_cached_cw_ids()
