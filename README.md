# pydollarmacro

## usage:

```
>>> import pydollarmacro
>>> pydollarmacro.subst_str_all("The $(speed=quick) $(color=brown) $(animal) $(blank=) $(a=(etc...\))",{"color": "orange", "animal": "dog"})
'The quick orange dog  (etc...)'
```
