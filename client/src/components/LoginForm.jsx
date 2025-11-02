import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";

const LoginForm = () => {
  const [showPassword, setShowPassword] = useState(false);
  const { register, handleSubmit, formState } = useForm();

  const onSubmit = async (data) => {
    console.log(data);
  };

  return (
    <div className="w-full space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <div className="flex justify-center mb-4">
          <div className="flex items-center gap-2 text-blue-600 font-bold text-lg">
            <span className="text-2xl">🎓</span>
            <span>EduApp</span>
          </div>
        </div>
        <h1 className="text-xl font-bold text-gray-900">Bienvenido de nuevo</h1>
        <p className="text-blue-600 text-sm font-medium">
          Por favor, inicie sesión para continuar
        </p>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {/* Email Field */}
        <div className="space-y-2">
          <label
            htmlFor="email"
            className="block text-gray-700 font-medium text-sm"
          >
            Usuario:
          </label>
          <input
            {...register("email")}
            id="email"
            type="email"
            placeholder="example@example.com"
            className={`w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              formState.errors.email ? "border-red-500" : "border-gray-300"
            }`}
          />
          {formState.errors.email && (
            <p className="text-red-500 text-xs">{formState.errors.email}</p>
          )}
        </div>

        {/* Password Field */}
        <div className="space-y-2">
          <label
            htmlFor="password"
            className="block text-gray-700 font-medium text-sm"
          >
            Correo:
          </label>
          <div className="relative">
            <input
              {...register("password")}
              id="password"
              type={showPassword ? "text" : "password"}
              placeholder="••••••••••"
              className={`w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                formState.errors.password ? "border-red-500" : "border-gray-300"
              }`}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              aria-label={
                showPassword ? "Ocultar contraseña" : "Mostrar contraseña"
              }
            >
              {showPassword ? "🙈" : "👁️"}
            </button>
          </div>
          {formState.errors.password && (
            <p className="text-red-500 text-xs">{formState.errors.password}</p>
          )}
        </div>

        {/* Forgot Password Link */}
        <div className="text-right">
          <Link
            to="/forgot-password"
            className="text-blue-600 hover:text-blue-700 text-sm font-medium"
          >
            ¿Olvidó su contraseña?
          </Link>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={formState.isSubmitting}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-2 rounded-md transition-colors"
        >
          {formState.isSubmitting ? "Iniciando sesión..." : "Iniciar sesión"}
        </button>
      </form>

      {/* Register Link */}
      <div className="text-center text-sm text-gray-600">
        <span>
          <Link
            to="/register"
            className="text-blue-600 hover:text-blue-700 font-medium"
          >
            Regístrate
          </Link>
          {" - "}
          <Link
            to="/dashboard"
            className="text-blue-600 hover:text-blue-700 font-medium"
          >
            Continuar
          </Link>
        </span>
      </div>
    </div>
  );
};

export default LoginForm;
