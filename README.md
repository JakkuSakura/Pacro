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

## Parser
```text

config_block = [config_comment (line) ] +
code_block = config_block? [whitespace * code_comment (line) ] +
line = char * newline
text_block = line +


```

## TODO
- [ ] Macro function call `macro_fun(example)` or `macro_fun!(example)`


