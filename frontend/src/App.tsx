import { GoogleOAuthProvider } from "@react-oauth/google";
import Auth from "./auth/auth";
import getAPI from "./functions/getAPI";
import React, { useEffect } from "react";
import Cookies from "cookiejs";
import NavBar from "./components/navBar";
import Hero from "./components/hero";
import CreateSummary from "./components/createSummary";
import ShowStock from "./components/showData";

function App() {
  const [auth, setAuth] = React.useState(false);

  const checkAuth = async () => {
    const user = Cookies.get("user");
    if (user) {
      setAuth(true);
    }
  };

  useEffect(() => {
    checkAuth();
  }, []);

  const [checkDataCreatedToday, setCheckDataCreatedToday] =
    React.useState(Boolean);

  const [DataCreatedToday, setDataCreatedToday] = React.useState(JSON);

  const checkCreatedTodayCall = async () => {
    const data = await getAPI({ url: "check/created/today" });
    if (data == false) {
      console.log("No data created today");
      setCheckDataCreatedToday(false);
    } else {
      console.log("Data created today");
      delete data.date;
      console.log(data);
      setCheckDataCreatedToday(true);
      setDataCreatedToday(data);
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
