import collections
from cpu import cpu_list

add = lambda a, b: a + b
sub = lambda a, b: a - b
mul = lambda a, b: a * b
div = lambda a, b: a / b

def pairwise_operation(func, A, B):
  return list(map(lambda t: func(t[0], t[1]), zip(A, B)))

def onetomany_operation(func, A, b):
  return list(map(lambda a: func(a, b), A))

def unary_operation(func, A):
  return list(map(func, A))

class SimpleMovingAverageMap:

  def __init__(self, func, sample_count):
    self.func = func
    self.sample_count = sample_count
    self.queue = collections.deque()
    self.sum = 0
  
  def __call__(self):
    sample = list(map(int, self.func()))
    if len(self.queue) == 0:
      self.sum = sample
    else:
      self.sum = pairwise_operation(add, self.sum, sample)
    self.queue.append(sample)
    while len(self.queue) > self.sample_count:
      self.sum = pairwise_operation(sub, self.sum, self.queue.popleft())
    return onetomany_operation(div, self.sum, len(self.queue))

def generate_metrics(sma_samples=1, cpu_indices=[0]):

  cpu_load_i = SimpleMovingAverageMap(
    lambda: onetomany_operation(
      mul,
      [
        load
        for i in cpu_indices
        for load in cpu_list[i].loads()
      ],
      100
    ),
    sma_samples
  )

  cpu_temperature_i = SimpleMovingAverageMap(
    lambda: onetomany_operation(
      mul,
      [
        temp
        for i in cpu_indices
        for temp in cpu_list[i].temperatures()
      ],
      10
    ),
    sma_samples
  )

  return {
    "cpu_load": lambda: onetomany_operation(div, cpu_load_i(), 10000),
    "cpu_temperature": lambda: onetomany_operation(div, cpu_temperature_i(), 10),
  }
