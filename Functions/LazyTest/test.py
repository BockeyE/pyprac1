class Circle(object):
    def __init__(self, radius):
        self.radius = radius

    # 加上property作注解后，可以直接点出来，
    # 不需要加括号，换句话说当成属性值调用
    @property
    def area(self):
        return 3.14 * self.radius ** 2


c = Circle(4)
print(c.radius)
print(c.area)


class lazy(object):
    def __init__(self, func):
        self.func = func

    # 一般来说, 描述符是带有“绑定行为”的对象属性,
    # 它的属性访问已经被描述符协议中的方法覆盖了.
    # 这些方法是__get__(), __set__(), 和__delete__().
    # 如果一个对象定义了这些方法中的任何一个, 它就是一个描述符.

    # object.__getattr__(self, name)
    # 当一般位置找不到attribute的时候，会调用getattr，
    # 返回一个值或AttributeError异常。

    # object.__getattribute__(self, name)
    # 无条件被调用，通过实例访问属性。
    # 如果class中定义了__getattr__()，则__getattr__()
    # 不会被调用（除非显示调用或引发AttributeError异常）

    # object.__get__(self, instance, owner)
    # 如果class定义了它，
    # 则这个class就可以称为descriptor。owner是所有者的类，
    # instance是访问descriptor的实例，如果不是通过实例访问，
    # 而是通过类访问的话，instance则为None。
    # （descriptor的实例自己访问自己是不会触发__get__，
    # 而会触发__call__，只有descriptor作为其它类的属性才有意义。）
    # （所以下文的d是作为C2的一个属性被调用）

    # 小结：可以看出，每次通过实例访问属性，
    # 都会经过__getattribute__函数。而当属性不存在时，
    # 仍然需要访问__getattribute__，不过接着要访问__getattr__。
    # 这就好像是一个异常处理函数。

    # 每次访问descriptor（即实现了__get__的类），
    # 都会先经过__get__函数。

    # 需要注意的是，当使用类访问不存在的变量是，
    # 不会经过__getattr__函数。而descriptor不存在此问题，
    # 只是把instance标识为none而已。
    def __get__(self, instance, cls):
        val = self.func(instance)
        setattr(instance, self.func.__name__, val)
        return val


class Circle(object):
    def __init__(self, radius):
        self.radius = radius

    # 在lazy类中，我们定义了__get__()
    # 方法，所以它是一个描述符。当我们第一次执行c.area时，
    # python解释器会先从c.__dict__中进行查找，没有找到，
    # 就从Circle.__dict__中进行查找，这时因为area被定义为描述符，
    # 所以调用__get__方法。

    # 在__get__()
    # 方法中，调用实例的area()
    # 方法计算出结果，并动态给实例添加一个同名属性area，
    # 然后将计算出的值赋予给它，
    # 相当于设置c.__dict__['area'] = val。

    # 当我们再次调用c.area时，直接从c.__dict__中进行查找，
    # 这时就会直接返回之前计算好的值了。
    @lazy
    def area(self):
        print('evalute')
        return 3.14 * self.radius ** 2


c = Circle(4)
print(c.radius)
print(c.area)
print(c.area)
print(c.area)
