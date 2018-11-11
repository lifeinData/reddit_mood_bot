import multiprocessing

def calc_square(numbers, q):

    for n in numbers:
        q.put (n*n)

def calc_cube(numbers):
    for n in numbers:
        print('cube ' + str(n*n*n))


if __name__ == '__main__':
    arr = [2,3,8]
    q = multiprocessing.Queue()
    result = multiprocessing.Array('i', 3)
    value = multiprocessing.Value('d', 0.0)
    p1 = multiprocessing.Process(target=calc_square, args=(arr,q))
    #p2 = multiprocessing.Process(target=calc_cube, args=(arr,))

    p1.start()
   # p2.start()

    p1.join()
    #p2.join()

    while q.empty() is False:
        print (q.get())
