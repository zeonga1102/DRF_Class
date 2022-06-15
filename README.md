# DRF
###  1. args, kwargs를 사용하는 예제 코드
```python
def my_function(*args, **kwargs):
    print('args: ', args)
    print('kwargs: ', kwargs)

my_list = [1, 2, 3, 4, 5]
my_dict = {'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}
my_function(*my_list, **my_dict)

# args:  (1, 2, 3, 4, 5)
# kwargs:  {'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}

my_function(1, 2, 3, 4, 5, key1='val1', key2='val2', key3='val3')

# args:  (1, 2, 3, 4, 5)
# kwargs:  {'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}

```
<br/>

### 2. mutable vs immutable
mutable은 수정 가능한 객체이고 immutable은 수정이 불가능한 객체이다.<br>
mutable 객체를 대입 연산자를 이용해 다른 변수에 넣어주면 얕은 복사가 발생한다.
따라서 같은 mutable 객체를 가리키는 경우 하나에서만 객체를 수정해도 수정 사항을 모두 공유한다.<br>
immutable 객체는 mutable 연산자와 달리 깊은 복사가 발생하므로 변수를 수정해도
바뀐 값을 공유하지 않는다.

<li>mutable object: int, float string, tuple 등</li>
<li>immutable object: list, dictionar</li>

<br/>

### 3. DB Field에서 사용되는 Key 종류와 특징
<li>FK: foreign key, 다른 테이블을 참조할 때 사용된다. 참조할 테이블의 PK를 바라본다.</li>
<li>UK: unique key, 중복 값을 허용하지 않는다. 테이블에 여러개가 존재할 수 있다.</li>
<li>PK: primary key, 테이블에 반드시 한개 존재해야하며 중복을 허용하지 않는다.</li>

<br/>

### 4. QuerySet vs Object
<li>queryset: 데이터베이스의 row, record에 해당한다. row들의 list이다.
values() 메소드를 사용해서 queryset에 있는 object들을 dictionary 형태로 만들 수 있다.
filter()와 all() 메소드의 반환값이 queryset 형태이다.

<li>object: 말 그대로 객체이다. 일반적인 클래스들의 객체와 같다. 모델의 객체라고 해서
속성이나 메소드에 접근하는 방식이 다른 것은 아니다. 데이터베이스의 관점에서 하나의 row에 해당하며 필드명들이 클래스의 멤버 변수로
선언되어 있기 때문에 .을 사용해서 원하는 필드의 값에 접근할 수 있다. get() 메소드의 반환값이 object이다.
