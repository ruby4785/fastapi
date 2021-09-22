from fastapi import FastAPI, File, UploadFile, responses
# from deta import Drive
from deta import Deta
deta = Deta("c0vgvnpj_4CjoaAYDXWuuC2CpC5iMPp9haP7GAw8J")
files= deta.Drive("s12")
# files = Drive("bus_video_storage_api") #Uncomment for local
app = FastAPI()


@app.post("/bus_id/{bus_id}/bus_date/{bus_date}/")
async def upload(bus_id,bus_date,file: UploadFile = File(...)):
    filenameextension= "."+file.filename.split(".")[1]
    name = str(bus_id)+"_"+str(bus_date)+filenameextension
    return files.put(name, file.file)

@app.get("/")
def list_files():
    return files.list()

@app.get("/bus_id/{bus_id}/bus_date/{bus_date}/")
async def serve(bus_id, bus_date):
    files_list = files.list()['names']
    name = str(bus_id)+"_"+str(bus_date)
    flag=0
    for i in files_list:
        if name in i:
            name=i
            flag=1
            break

    if flag == 0:
        return {"items":"No items found"}
    # return name
    img = files.get(name)
    #
    if img != None:
        return responses.StreamingResponse(img.iter_chunks(1024), media_type="video/mp4") 

@app.delete('/bus_id/{bus_id}/bus_date/{bus_date}/')
async def delete(bus_id,bus_date):
    name = bus_id + "_" + bus_date
    return files.delete(name)

@app.delete('/')
async def deleteall():
    return files.delete_many(files.list()["names"])


# if __name__ == '__main__':
#     # start the flask app
#     uvicorn.run(app, host="127.0.0.1", port=8001, access_log=False)

