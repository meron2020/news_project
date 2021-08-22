const fetch = require('node-fetch')


const ServerConnection = {
    url: "http://127.0.0.1:5000/",

    async getNews(topic) {
        try {
            const response = await fetch(`${ServerConnection.url}news/${topic}`,
                {headers: {"connection": "keep-alive"}})
            if (response.ok) {
                let responseJson =  await response.json();
                return responseJson["rows_list"];
            }
            throw new Error("Request failed!");
        }
        catch(error) {
            document.write(error)
        }
        }
}
export default ServerConnection