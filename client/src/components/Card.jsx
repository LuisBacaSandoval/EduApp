import { Link } from "react-router-dom";

export default function Card({ title, subtitle, image, features = [], to, linkText = "Ver más ..." }) {

    return (
        <div className="bg-white rounded-lg border-2 border-purple-200 p-4 hover:shadow-lg transition-shadow duration-300">
            <div className="flex gap-4">
                {/* Image Section */}
                <div className="shrink-0">
                    <img className="w-32 h-32 rounded-lg overflow-hidden bg-linear-to-br from-gray-100 to-gray-200" src={image} />
                </div>

                {/* Content Section */}
                <div className="flex-1 flex flex-col">
                    <h3 className={'text-xl font-bold text-blue-600 mb-1'}>
                        {title}
                    </h3>
                    <p className="text-sm text-indigo-400 font-semibold mb-3">
                        {subtitle}
                    </p>

                    {/* Features */}
                    <div className="flex-1">
                        {features.map((feature, index) => (
                            <p key={index} className="text-sm text-gray-800 mb-1">
                                {feature}
                            </p>
                        ))}
                    </div>

                    {/* Link */}
                    <div className="mt-auto pt-2">
                        <Link
                            to={to || "#"}
                            className={'text-sm text-blue-600 hover:underline inline-flex items-center'}
                        >
                            {linkText}
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
};