import re

def find_right_paren(s, start=0):
	m = re.search("(^|[^\\\])[)]",s[start:])
	if m is None:
		return None
	return start + m.end() - 1

def get_first_outer_macro(s):
	left = s.find("$(")
	left2 = s.find("$(", left+1)
	right = find_right_paren(s, 0)
	while right is not None and left2<right and left2!=-1:
		gfom = get_first_outer_macro(s[left2:])
		n = left2+len(gfom)
		right = find_right_paren(s, n)
		left2 = s.find("$(", left2+len(gfom))
	if right is None:
		return None
	return s[left:right+1]

def call_until_invariant(f, args):
	x = args[0]
	if f(*args)==x:
		return x
	return f(*args)

def macro_name(s):
	gfom = get_first_outer_macro(s)
	if gfom is None:
		return None
	return gfom[2:-1].split("=")[0]

def get_macro_by_name(s, name):
	i = s.find("$(")
	while(i!=-1):
		if macro_name(s[i:]) == name:
			return get_first_outer_macro(s[i:])
		i = s.find("$(",i+1)
	return None

def subst_str_once(s, macros):
	for m_k in macros.keys():
		if get_macro_by_name(s, m_k) is not None:
			s = s.replace(get_macro_by_name(s, m_k), macros[m_k])
	return s.replace("\)",")")


def subst_str(s, macros):
	return call_until_invariant(subst_str_once, [s, macros])

def subst_str_defaults_once(s):
	m = get_first_outer_macro(s)
	if m is None:
		return s
	v = m.split("=")[1][:-1]
	return s.replace(m, v)

def subst_str_defaults(s):
	return call_until_invariant(subst_str_defaults_once, [s])

def subst_str_all(s, macros):
	s = subst_str(s, macros)
	return subst_str_defaults(s)

