# Pacro
Powerful embedded macro implemented in Python for all languages.

## Example
```c++
//% Lang: Python
//$ code("int foo(){}");
int main() {

}
```
it will convert to 
```c++
//% Lang: Python
//% Hash: ABCDEFG
//$ code("int foo(){}");
//######################
int foo(){};
//^^^^^^^^^^^^^^^^^^^^^^
int main() {

}
```

## Lexer
```text
config_comment = '//%'
code_comment = '//$'

newline = ['\r\n', '\n']
char = *
```
