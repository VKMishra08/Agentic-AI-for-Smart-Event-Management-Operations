import asyncio
import os
import statistics
import time
import httpx

URL=os.getenv('EVENTOPS_BASE_URL','http://127.0.0.1:5000')
CONCURRENCY=int(os.getenv('BENCHMARK_CONCURRENCY','8'))
REQUESTS=int(os.getenv('BENCHMARK_REQUESTS','40'))

async def one(client):
    start=time.perf_counter()
    r=await client.get('/api/performance')
    r.raise_for_status()
    return (time.perf_counter()-start)*1000

async def main():
    limits=httpx.Limits(max_connections=CONCURRENCY)
    async with httpx.AsyncClient(base_url=URL,limits=limits,timeout=20) as client:
        sem=asyncio.Semaphore(CONCURRENCY)
        async def wrapped():
            async with sem: return await one(client)
        values=await asyncio.gather(*(wrapped() for _ in range(REQUESTS)))
    values.sort()
    p95=values[min(len(values)-1,int(len(values)*0.95))]
    print({'requests':REQUESTS,'concurrency':CONCURRENCY,'average_ms':round(statistics.mean(values),2),'p95_ms':round(p95,2),'min_ms':round(min(values),2),'max_ms':round(max(values),2)})

if __name__=='__main__': asyncio.run(main())
