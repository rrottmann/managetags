# managetags
Python script to manage tags encoded in the filename.

A tag is kept in a list of keywords enclosed in '[' and ']'
at the end of the filename - just before the file extension.

Tags may be used to organize the file and to easier locate it.

See also: https://github.com/rrottmann/filewrangler

# Usage

~~~
$ ./managetags.py --help
usage: managetags.py [-h] [--debug] [--nopreserve] [--nosorttags]
                     [--notagctime] --path PATH [--quiet] [--addtags ADDTAGS]
                     [--removetags REMOVETAGS]

optional arguments:
  -h, --help            show this help message and exit
  --debug               Enable debug output.
  --nopreserve          Do not preserve original tags.
  --nosorttags          Do not sort tags.
  --notagctime          Do not add tag for ctime.
  --path PATH           Path to file/dir to tag.
  --quiet               Quiet mode.
  --addtags ADDTAGS     Comma seperated list of tags to add.
  --removetags REMOVETAGS
                        Comma seperated list of tags to remove.
~~~

# Examples

## Add file's creation time as tag

 * Create a test file

~~~
touch test.txt
~~~

 * Run managetags only with the path argument and see that a ctime tag gets proposed

~~~
 ./managetags.py --path test.txt
mv "test.txt" "test [170106].txt"
~~~

 * As you are pleased with the result, we now execute the generated commands.

~~~
$ ./managetags.py --path test.txt | sh -x
+ mv test.txt 'test [170106].txt'
ls -la test*
-rw-r--r--. 1 root root 0 Jan  6 06:14 test [170106].txt
~~~

## Add tags 'foo', 'bar' and 'baz'

  * Add 'foo' and 'bar' first

~~~
$ ./managetags.py --path "test [170106].txt" --addtags 'foo,bar'
mv "test [170106].txt" "test [170106 bar foo].txt"
~~~

 * As you are pleased with the result, we now execute the generated commands.

~~~
$ ./managetags.py --path "test [170106].txt" --addtags 'foo,bar' | sh -x
+ mv 'test [170106].txt' 'test [170106 bar foo].txt'
$ ls -al test*
-rw-r--r--. 1 root root 0 Jan  6 06:14 test [170106 bar foo].txt

 * Now add the tag 'baz' but we also want to remove the ctime tag. We want also debug output

~~~
$ ./managetags.py --path "test [170106 bar foo].txt" --addtags 'baz' --removetags '170106' --notagctime --debug
#DEBUG: File has been tagged before.
#DEBUG: Using old tags: 170106,bar,foo
#DEBUG: Adding tag: baz
#DEBUG: Removing tag: 170106
#DEBUG: Sorting tags.
mv "test [170106 bar foo].txt" "test [bar baz foo].txt"
~~~

 * As we are happy with it, we execute the generated commands. Note the debug output gets ignored.

~~~
./managetags.py --path "test [170106 bar foo].txt" --addtags 'baz' --removetags '170106' --notagctime --debug | sh -x
#DEBUG: File has been tagged before.
#DEBUG: Using old tags: 170106,bar,foo
#DEBUG: Adding tag: baz
#DEBUG: Removing tag: 170106
#DEBUG: Sorting tags.
+ mv 'test [170106 bar foo].txt' 'test [bar baz foo].txt'
~~~

 * Inspect the results

~~~
$ ls -al test*
-rw-r--r--. 1 root root 0 Jan  6 06:14 test [bar baz foo].txt
~~~
