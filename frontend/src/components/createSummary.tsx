import { useState, useEffect } from "react";
import getAPI from "../functions/getAPI";
<<<<<<< HEAD
import ShowStock from "./showData";
=======
>>>>>>> 0a0662676ea2ca5ef2b8eac4b75e1ba2fcb82ee4

function CreateSummary() {
  const [loading, setLoading] = useState(false);
  const [taskID, setTaskID] = useState("");
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("");
  const [result, setResult] = useState(null);

  const handleCreateSummary = async () => {
    setLoading(true);
    setProgress(0);
    setStatus("Starting task...");
    const data = await getAPI({ url: "create/today" });

    if (data["task_id"]) {
      setTaskID(data["task_id"]);
<<<<<<< HEAD
    } else if (data["error"]) {
      setTaskID("");
      setLoading(false);
      return alert(data["error"]);
=======
>>>>>>> 0a0662676ea2ca5ef2b8eac4b75e1ba2fcb82ee4
    } else {
      setTaskID("");
      setLoading(false);
    }
  };

  const checkTaskStatus = async () => {
    if (taskID) {
      const data = await getAPI({ url: `task_status/${taskID}` });
      setStatus(data.state);
      setProgress(data.progress);

      if (data.state === "SUCCESS") {
<<<<<<< HEAD
        setLoading(false);
        window.location.reload();
=======
        setResult(data.result);
        setLoading(false);
>>>>>>> 0a0662676ea2ca5ef2b8eac4b75e1ba2fcb82ee4
      }
    }
  };

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (taskID && !result) {
      interval = setInterval(() => checkTaskStatus(), 2000);
    }
    return () => clearInterval(interval);
  }, [taskID, result]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="hero p-6">
        {status === "SUCCESS" && result ? (
<<<<<<< HEAD
          <ShowStock data={result} />
=======
          <h1 className="mt-4 text-3xl font-bold text-primary">
            Task completed successfully! {JSON.stringify(result)}
          </h1>
>>>>>>> 0a0662676ea2ca5ef2b8eac4b75e1ba2fcb82ee4
        ) : (
          <>
            {!loading && (
              <button
                className="btn btn-primary mb-4"
                onClick={handleCreateSummary}
                disabled={loading}
              >
                {taskID ? `Task ID: ${taskID}` : "Create Summary"}
              </button>
            )}

            {loading && (
              <div className="w-1/2 backdrop-blur-xl rounded-lg p-4 border border-gray-300">
                <div className="flex justify-between mb-2">
                  <span className="text-sm">Status: {status}</span>
                  <span className="text-sm">{progress}%</span>
                </div>

                <progress
                  className="progress progress-primary w-full"
                  value={progress}
                  max="100"
                ></progress>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default CreateSummary;
