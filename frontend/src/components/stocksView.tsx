interface stocksViewProps {
  data: JSON | any;
}

function stocksView({ data }: stocksViewProps) {
  return (
    <div>
      <h1>Stocks Data</h1>
      <ul>
        {Object.keys(data).map((key) => (
          <li key={key}>
            {key}: {data[key]}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default stocksView;
