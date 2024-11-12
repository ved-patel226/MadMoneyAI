import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Register the required components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface showDataProps {
  data: { [key: string]: string[] | string | { [key: string]: string } };
}

function ShowStock({ data }: showDataProps) {
  return (
    <div className="space-y-4">
      {Object.entries(data).map(([key, value]) => {
        // Assuming value is an array of stock data for the graph
        const chartData = Array.isArray(value)
          ? {
              labels: value.map((_, index) => `Day ${index + 1}`), // Adjust according to your data
              datasets: [
                {
                  label: key,
                  data: value.map((val) => parseFloat(val)), // Assuming value is a price or number
                  borderColor: "#20B2AA",
                  backgroundColor: "rgba(32, 178, 170, 0.2)",
                  fill: true,
                },
              ],
            }
          : {};

        return (
          <div key={key} className="flex flex-col gap-5">
            <h1 className="text-xl font-semibold">{key}</h1>
            {Array.isArray(value) && value.length > 0 && (
              <Line
                data={chartData}
                options={{
                  responsive: true,
                  plugins: { legend: { position: "top" } },
                }}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}

export default ShowStock;
