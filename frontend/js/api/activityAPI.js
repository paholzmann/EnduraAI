const activityUrl = "http://127.0.0.1:8000/api/v1/activity/summary";

export async function getActivitySummary(file) {
    const formData = new FormData();

    formData.append(
        "file",
        file
    );

    const response = await fetch(
        activityUrl,
        {
            method: "POST",
            body: formData
        }
    );

    if (!response.ok) {
        throw new Error("Activity summary failed");
    }

    return await response.json();
}