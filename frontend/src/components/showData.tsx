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
import React, { useState, useEffect } from "react";

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
  const [stockData, setStockData] = useState<any[]>([]);

  console.log("data", data["GOOG"]);

  const stockDataCall = async () => {
    const response = await getAPI({ url: "get/recent" });
    if (response["prices"]) {
      const newData = response["prices"].map((price: any[]) => ({
        symbol: price[0],
        prices: price[1],
      }));
      setStockData((prevData) => [...prevData, ...newData]);
      console.log(newData);
    }
  };

  useEffect(() => {
    stockDataCall();
  }, []);

  return (
    <div className="space-y-4">
      <div className="flex flex-row w-full justify-center flex-wrap gap-5">
        {stockData.length > 0 &&
          stockData.map((stock, index) => (
            <div
              key={index}
              className="flex flex-col gap-5 w-1/4 border border-primary p-5 rounded-lg"
            >
              <div className="flex flex-row justify-center items-center gap-5">
                <h1 className="text-[50px] font-semibold">{stock.symbol}</h1>
                {data[stock.symbol] && (
                  <h1 className="badge badge-primary ml-2 text-[20px] p-[20px]">
                    {Array.isArray(data[stock.symbol])
                      ? (data[stock.symbol][0] as string[])
                      : typeof data[stock.symbol] === "object"
                      ? JSON.stringify(data[stock.symbol])
                      : String(data[stock.symbol])}
                  </h1>
                )}
              </div>

              <Line
                data={{
                  labels: stock.prices.map(
                    (_: number, index: number) => `Day ${index + 1}`
                  ),
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
            </div>
          ))}
      </div>
    </div>
  );
}

export default ShowStock;
