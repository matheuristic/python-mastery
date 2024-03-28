def typedproperty(name, expected_type):
    private_name = '_' + name

    @property
    def value(self):
        return getattr(self, private_name)

    @value.setter
    def value(self, val):
        if not isinstance(val, expected_type):
            raise TypeError(f'Expected {expected_type}')
        setattr(self, private_name, val)
   
    return value

String = lambda name: typedproperty(name, str)
Integer = lambda name: typedproperty(name, int)
Float = lambda name: typedproperty(name, float)

# ex5_4_c

# Not quite sure if this is what the exercise intended
# Assume we care about the metaprogramming but don't need to keep the return value as a property function with a setter

def typedproperty2(expected_type):
    class TypedMetaclass:
        expectedtype = expected_type

        def __set_name__(self, cls, name):
            self.name = name
        
        @classmethod    
        def check(cls, value):
            if not isinstance(value, cls.expectedtype):
                raise TypeError(f'Expected {cls.expectedtype}')
            return value
        
        def __set__(self, instance, value):
            instance.__dict__[self.name] = self.check(value)
            
    return TypedMetaclass

String2 = typedproperty2(str)
Integer2 = typedproperty2(int)
Float2 = typedproperty2(float)
