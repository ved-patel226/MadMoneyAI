interface PropsHero {
  first: boolean;
}

function Hero({ first }: PropsHero) {
  return (
    <div className="hero bg-base-200 min-h-screen">
      <div className="hero-content text-center">
        {first ? (
          <div className="max-w-md">
            <h1 className="text-5xl font-bold">
              Good News! It's already Summarized!
            </h1>
            <p className="py-6">Here are the Mad Money summaries for today:</p>
          </div>
        ) : (
          <div>
            <div className="max-w-md">
              <h1 className="text-5xl font-bold">
                No one created a Mad Money summary today..
              </h1>
              <p className="py-6">Login to create one</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Hero;
