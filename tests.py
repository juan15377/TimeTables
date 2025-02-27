import asyncio 

async def tarea_1():
    print('Tarea 1')
    await asyncio.sleep(1)
    print('Tarea 1 finalizada')
    print("segunda parte iniciada")
    await asyncio.sleep(2)
    print("segunda parte finalizada") 
    
async def tarea_2():
    print('Tarea 2')
    await asyncio.sleep(2)
    print('Tarea 2 finalizada') 
    
async def tarea_3():
    print('Tarea 3')
    await asyncio.sleep(3)
    print('Tarea 3 finalizada') 
    
    
async def main():
    await asyncio.gather(tarea_1(), tarea_2(), tarea_3())
    print('Todos los hilos han finalizado')
    
asyncio.run(main())