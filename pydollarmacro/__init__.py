import re

def get_first_outer_macro_old(s):
	left = s.find("$(")
	if left == -1:
		return ""
	left2 = s[left+2:].find("$(")
	if left2!=-1:
		left2 += left+2
	right = s.find(")")
	print("left2", left2, "right", right)
	while left2<right and left2!=-1:
		print("in loop")
		print(s[left2+1:])
		print("left2",left2, right)
		gfom = get_first_outer_macro(s[left2:])
		print(gfom)
		end2 = left2 + len(gfom)
		print("end2", end2)
		left2 = end2+1+s[end2+1:].find("$(")
		right = end2+1+s[end2+1:].find(")")
		if gfom=="":
			break
	
	#inner = get_first_outer_macro(s[start+1:])
	#n = s.find(inner)+len(inner)
	print(left,right)
	return s[left:right+1]
	
def find_right_paren(s, start=0):
	m = re.search("(^|[^\\\])[)]",s[start:])
	if m is None:
		return None
	return start + m.end() - 1

def get_first_outer_macro(s):
	left = s.find("$(")
	left2 = s.find("$(", left+1)
	#right = s.find(")")
	print(s)
	right = find_right_paren(s, 0)
	#right = re.search("(^|[^\\\])[)]",s).end() - 1
	while right is not None and left2<right and left2!=-1:
		gfom = get_first_outer_macro(s[left2:])
		#right = s.find(")", left2+len(gfom))
		n = left2+len(gfom)
		#right = n + re.search("(^|[^\\\])[)]",s[n:]).end() - 1
		right = find_right_paren(s, n)
		left2 = s.find("$(", left2+len(gfom))
	if right is None:
		return None
	return s[left:right+1]

#def replace_all_once(s, macros):
#	for 


def call_until_invariant(f, args):
	x = args[0]
	if f(*args)==x:
		return x
	return f(*args)

def find_first_macro(s, name=""):
	if name != "":
		name += "(?!\w)"
	r = re.search("\$[(]"+name+"(\\\[)]|[^)])*[)]", s)
	if r is None:
		return None
	return r.group()

def macro_name(s):
	return get_first_outer_macro(s)[2:-1].split("=")[0]

def get_macro_by_name(s, name):
	i = s.find("$(")
	while(i!=-1):
		if macro_name(s[i:]) == name:
			return get_first_outer_macro(s[i:])
		i = s.find("$(",i+1)
		print(i)
	return None
		
	

def subst_str_once(s, macros):
	for m_k in macros.keys():
		#print(s, m_k, find_first_macro(s, m_k))
		#s = s.replace("$("+m_k+")", macros[m_k])
		if get_macro_by_name(s, m_k) is not None:
			#s = s.replace(find_first_macro(s, m_k), macros[m_k])
			#s = s.replace(get_first_outer_macro(s), macros[m_k])
			s = s.replace(get_macro_by_name(s, m_k), macros[m_k])
			#print(s)
	return s.replace("\)",")")


def subst_str(s, macros):
	return call_until_invariant(subst_str_once, [s, macros])

def subst_str_defaults_once(s):
	#m = re.search("\$\(.*?\)", s)
	#m = re.search("\$[(](\\\[)]|[^)])+[)]", s).group().replace("\)",")")
	m = find_first_macro(s)
	if m is None:
		return s
	v = m.split("=")[1][:-1]
	return s.replace(m, v)

def subst_str_defaults(s):
	return call_until_invariant(subst_str_defaults_once, [s])

def subst_str_all(s, macros):
	s = subst_str(s, macros)
	return subst_str_defaults(s)

#print("abc$(de)fg".replace("$(de)","aaaa"))
d={"ded": "bbb", "a": "wwww"}
#s = subst_str("abc$(de=$(a\))fg",d)
s = subst_str("abc$(de=$(a))fg",d)
print("s", s)
s = subst_str_defaults(s)
print("ans", s)
