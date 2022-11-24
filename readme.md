tomcli
======

`tomcli` is a simple wrap python lib click, for create simple cli tools.
for example, I need rerun a compiler with different flags and execute with different flags

```
1: clang -O3 test.c -o a.out
2: clang -O2 test.c -o b.out
3: time a.out
4: time b.out
```

```test.toml
[commands]
build = "clang $opt test.c -o $exe
run = "time $exe"

[build]
[build.opt]
opt2="-O2"
opt3="-O3"

[exe]
a="a"
b="b"
```

and then
```
python3 cli.py test.toml build --opt=opt3 --exe=a
python3 cli.py test.toml build --opt=opt2 --exe=b
```

