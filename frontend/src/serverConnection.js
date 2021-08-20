const ServerConnection = {
    url: "http://localhost:5000/",

    async getNews() {
        try {
            const response = await fetch(`${ServerConnection.url}news/`,
                {headers: {"connection": "keep-alive", "content-type": "application/json"}})
            if (response.ok) {
                return await response.json()
            }
            throw new Error("Request failed!");
        }
        catch(error) {
            document.write(error)
        }
        }
    }
