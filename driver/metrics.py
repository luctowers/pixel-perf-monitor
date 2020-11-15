import collections
from cpu import cpu_list
from memory import memory_list
from gpu import gpu_list

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

  def __init__(self, sample_count, func):
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

def generate_float_sma_metric(sma_samples, precision, func):
  integer_metric = SimpleMovingAverageMap(
    sma_samples,
    lambda: onetomany_operation(
      div,
      func(),
      precision
    )
  )
  return lambda: onetomany_operation(mul, integer_metric(), precision)

def generate_metrics(sma_samples=1):

  return {
    "cpu_usage": generate_float_sma_metric(
      sma_samples, .001,
      lambda: [
        usage
        for cpu in cpu_list
        for usage in cpu.usages()
      ]
    ),
    "cpu_temperature": generate_float_sma_metric(
      sma_samples, .1,
      lambda: [
        temp
        for cpu in cpu_list
        for temp in cpu.temperatures()
      ]
    ),
    "cpu_memory_usage": generate_float_sma_metric(
      sma_samples, .001,
      lambda: [memory_list[0].usage()] if memory_list and memory_list[0].usage() != None else []
    ),
    "gpu_usage": generate_float_sma_metric(
      sma_samples, .001,
      lambda: [ gpu.usage() for gpu in gpu_list ]
    ),
    "gpu_temperature": generate_float_sma_metric(
      sma_samples, .001,
      lambda: [ gpu.temperature() for gpu in gpu_list ]
    ),
    "gpu_memory_usage": generate_float_sma_metric(
      sma_samples, .001,
      lambda: [ gpu.memory_usage() for gpu in gpu_list ]
    )
  }
