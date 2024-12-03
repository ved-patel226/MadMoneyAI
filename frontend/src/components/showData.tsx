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
import getAPI from "../functions/getAPI";
import { useState, useEffect } from "react";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

// Update the interface to match the actual data structure
interface StockData {
  [key: string]: [string, string, number[]]; // [action, description, prices]
}

interface ShowDataProps {
  data: StockData;
}

interface Stock {
  symbol: string;
  prices: number[];
}

function ShowStock({ data }: ShowDataProps) {
  const [stockData, setStockData] = useState<Stock[]>([]);

  const stockDataCall = async () => {
    try {
      const response = await getAPI({ url: "get/recent" });

      if (response["prices"]) {
        const newData = response["prices"].map((price: any[]) => ({
          symbol: price[0],
          prices: price[1],
        }));

        setStockData(newData);
      }
    } catch (error) {
      console.error("Error fetching stock data:", error);
    }
  };

  useEffect(() => {
    stockDataCall();
  }, []);

  return (
    <div className="space-y-4">
      <div className="flex flex-row w-full justify-center flex-wrap gap-5">
        {stockData.map((stock) => (
          <div
            key={stock.symbol}
            className="flex flex-col gap-5 w-1/2 border border-primary p-5 rounded-lg"
          >
            <div className="flex flex-row justify-center items-center gap-5">
              <h1 className="text-[50px] font-semibold">{stock.symbol}</h1>
              <h1
                className={`badge ml-2 text-[20px] p-[20px] ${
                  data[stock.symbol][0] === "buy"
                    ? "badge-success"
                    : data[stock.symbol][0] === "sell"
                    ? "badge-error"
                    : "badge-neutral"
                }`}
              >
                {data[stock.symbol][0]}
              </h1>
            </div>
            <Line
              data={{
                labels: stock.prices.map((_, index) => `Day ${index + 1}`),
                datasets: [
                  {
                    label: stock.symbol,
                    data: stock.prices,
                    borderColor: "#20B2AA",
                    backgroundColor: "rgba(32, 178, 170, 0.2)",
                    fill: true,
                  },
                ],
              }}
              options={{
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                  x: {
                    display: false,
                  },
                },
              }}
            />
            <h1>{data[stock.symbol][1]}</h1>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ShowStock;
