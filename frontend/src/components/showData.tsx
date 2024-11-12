interface showDataProps {
  data: { [key: string]: string[] | string | { [key: string]: string } };
}

function ShowStock({ data }: showDataProps) {
  return (
    <div className="space-y-4">
      {Object.entries(data).map(([key, value]) => {
        return (
          <div key={key} className="flex flex-row gap-5">
            <h1>{key}</h1>
            <h1>{value[0]}</h1>
          </div>
        );
      })}
    </div>
  );
}

export default ShowStock;
