import { useRoutes } from "react-router-dom";
import { routes } from "./routes";
import HandTracking from "./components/HandTracking";

function App() {
  const element = useRoutes(routes);

  return (
    <div>
      {element}
      {/* <div className="absolute z-50 bottom-0 right-0 w-[50vw] lg:w-[15vw] h-auto max-w-full overflow-hidden flex items-center justify-center bg-gray-100">
        <HandTracking />
        </div> */}
    </div>
  );
}

export default App;
