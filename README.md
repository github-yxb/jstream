# JStream
Is a simple tool like Java stream.

## install
pip install jstream

## example

``` python
from JStream import JStream, collectors

s = JStream([1,2,3,4,5,6,7,8,9,10])
s.filter(lambda x: x % 2 == 0).sum()

s.filter(lambda x: x >= 5).collect(collectors.GroupingByCollector(lambda x: x % 2))
```
