import { GoogleOAuthProvider } from "@react-oauth/google";
import Auth from "./auth/auth";
import getAPI from "./functions/getAPI";
import React, { useEffect } from "react";
<<<<<<< HEAD
import Cookies from "cookiejs";
import NavBar from "./components/navBar";
import Hero from "./components/hero";
import CreateSummary from "./components/createSummary";
import ShowStock from "./components/showData";
=======
import { get } from "http";
import Cookies from "cookiejs";
import NavBar from "./components/navBar";
import PlaceHolder from "./components/placeHolder";
import Hero from "./components/hero";
import stocksView from "./components/stocksView";
import CreateSummary from "./components/createSummary";
>>>>>>> 0a0662676ea2ca5ef2b8eac4b75e1ba2fcb82ee4

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

<<<<<<< HEAD
  const [DataCreatedToday, setDataCreatedToday] = React.useState(JSON);

=======
>>>>>>> 0a0662676ea2ca5ef2b8eac4b75e1ba2fcb82ee4
  const checkCreatedTodayCall = async () => {
    const data = await getAPI({ url: "check/created/today" });
    if (data == false) {
      console.log("No data created today");
      setCheckDataCreatedToday(false);
    } else {
      console.log("Data created today");
<<<<<<< HEAD
      delete data.date;
      console.log(data);
      setCheckDataCreatedToday(true);
      setDataCreatedToday(data);
    }
  };

  useEffect(() => {
    checkCreatedTodayCall();
  }, []);
=======
      setCheckDataCreatedToday(true);
    }
  };

  checkCreatedTodayCall();
>>>>>>> 0a0662676ea2ca5ef2b8eac4b75e1ba2fcb82ee4

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
<<<<<<< HEAD
          {checkDataCreatedToday ? (
            <ShowStock data={DataCreatedToday} />
          ) : (
            <>
              <CreateSummary />
            </>
          )}
=======
          <CreateSummary />
>>>>>>> 0a0662676ea2ca5ef2b8eac4b75e1ba2fcb82ee4
        </>
      ) : (
        <Hero first={checkDataCreatedToday} />
      )}
    </div>
  );
}

export default App;
