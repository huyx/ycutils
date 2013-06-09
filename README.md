# ycutils 库 #

## cacheit ##

特点：

 * 支持指定超时时间
 * 针对不指定超时时间的情况做了优化

用法:

    @cacheit()
    def f1():
        // ...

    @cacheit(3)
    def f2():
        // ...

## batchit ##

允许用户提供一个批处理函数，批量处理操作

* 支持批量操作
* 用户可以随时调用 func.batch 批量执行操作

用法：

    def batch_op(batch_args):
        for args, kwargs in batch_args:
            print args, kwargs

    @batchit(batch_op, 10, 10)
    def op(*args, **kwargs):
        print args, kwargs

## echoit ##

原来的 README 参见 README.echo.txt

这个在原来的基础上增加了两个参数的定制：

    echo 模块
        setup(write, method)

使用例子(使用在 Twisted 中)：

    from twisted.python import log
	import echo
	
	echo.setup(log.msg, '')

## basex ##

任意进制（<=256）转换：

    codec = BaseX("13579")
    codec.encode(100)
	codec.decode("1")			# 0
	codec.decode("13")			# 1
