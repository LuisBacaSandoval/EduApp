import firstImage from "../assets/first-image.avif";
import LoginForm from "../components/LoginForm";

const Home = () => {
  return (
    <>
      <div className="flex min-h-screen">
        {/* Left side - Blue section with text */}
        <div className="hidden lg:flex w-1/2 bg-primary items-center justify-center p-8">
          <div className="text-white max-w-2xl">
            <h1 className="w-full text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl font-bold leading-tight md:leading-snug text-center lg:text-left">
              Un nuevo nivel de aprendizaje
              <br className="hidden sm:block" />
              personalizado.
            </h1>
          </div>
        </div>

        {/* Right side - Form section with background image */}
        <div
          className="w-full lg:w-1/2 bg-cover bg-center relative flex items-center justify-center p-6"
          style={{
            backgroundImage: `url(${firstImage})`,
          }}
        ></div>
      </div>
      <div className="fixed inset-0 z-50 flex items-center justify-center">
        <div className="w-full max-w-md p-4 bg-white rounded-lg">
          <LoginForm />
        </div>
      </div>
    </>
  );
};

export default Home;
