import { GoogleOAuthProvider } from "@react-oauth/google";
import Auth from "./auth/auth";
import getAPI from "./functions/getAPI";
import { useEffect, useState } from "react";
import Cookies from "cookiejs";
import NavBar from "./components/navBar";
import Hero from "./components/hero";
import CreateSummary from "./components/createSummary";
import ShowStock from "./components/showData";

// Define the type for stock data to match the interface in showData.tsx
interface StockData {
  [key: string]: [string, string, number[]];
}

function App() {
  const [auth, setAuth] = useState(false);

  const checkAuth = async () => {
    const user = Cookies.get("user");
    if (user) {
      setAuth(true);
    }
  };

  useEffect(() => {
    checkAuth();
  }, []);

  const [checkDataCreatedToday, setCheckDataCreatedToday] = useState(false);
  const [DataCreatedToday, setDataCreatedToday] = useState<StockData>({});

  const checkCreatedTodayCall = async () => {
    const data = await getAPI({ url: "check/created/today" });
    if (data === false) {
      console.log("No data created today");
      setCheckDataCreatedToday(false);
    } else {
      delete data.date;
      console.log("Stock Recommendation data: ", data);
      setCheckDataCreatedToday(true);
      setDataCreatedToday(data as StockData);
    }
  };

  useEffect(() => {
    checkCreatedTodayCall();
  }, []);

  return (
    <div className="App">
      <NavBar>
        <header className="App-header inline-flex w-fit h-fit">
          <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
            <Auth />
          </GoogleOAuthProvider>
        </header>
      </NavBar>
      {auth ? (
        <>
          {checkDataCreatedToday ? (
            <ShowStock data={DataCreatedToday} />
          ) : (
            <>
              <CreateSummary />
            </>
          )}
        </>
      ) : (
        <Hero first={checkDataCreatedToday} />
      )}
    </div>
  );
}

export default App;
