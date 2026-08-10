type FeatureCardProps = {
  title: string;
  description: string;
};

export default function FeatureCard({
  title,
  description,
}: FeatureCardProps) {
  return (
    <div className="border p-4 rounded-lg">
      <h3 className="font-bold">{title}</h3>

      <p>{description}</p>
    </div>
  );
}