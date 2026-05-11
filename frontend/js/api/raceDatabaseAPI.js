
const raceDatabaseUrl = "http://127.0.0.1:8000/api/v1/race_database/get_race_database";

export async function getRaceDatabase(limit, offset) {
    try {
        const response = await fetch(raceDatabaseUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                limit: limit,
                offset: offset
            })
        });
        if (!response.ok) {
            throw new Error("Request failed");
        }
        const data = await response.json();
        return data
    } catch (error) {
        console.error(error);
    }
}