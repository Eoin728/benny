import http.client
import json


def transcribe(f):

    key = "8cf77b5e01365444aacb96be492fcdf75d562952"
    headers = {"Authorization": "Token " + key, "Content-Type": "audio/*"}
    audiofilepath = "DM.wav"
    url = "api.deepgram.com"
    data = f.read()

    conn = http.client.HTTPSConnection(url)

    # Define the request body
    body = data

    # Send the POST request
    conn.request("POST", "/v1/listen", body, headers)

    # Get the response
    response = conn.getresponse()

    # Read and print the response data
    response_data = response.read()
    # file = open("idkman.json", "w")
    # file2 = open(storage_file, "w")
    j = json.loads(response_data)
    # print(json.loads(response_data))
    t = j["results"]["channels"][0]["alternatives"][0]["transcript"]

    # json.dump(j, file)
    # file2.write(t)
    conn.close()
    return t
