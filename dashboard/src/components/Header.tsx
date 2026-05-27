type Props = { restaurantName: string | null };

export function Header({ restaurantName }: Props) {
  return (
    <header className="border-b border-beige-deep bg-beige-card">
      <div className="max-w-[1600px] mx-auto px-8 py-6 flex items-baseline justify-between">
        <div>
          <p className="text-sm uppercase tracking-wider text-ink-mute">
            AlToque · Dashboard
          </p>
          <h1 className="text-3xl font-semibold text-ink mt-1">
            {restaurantName ?? "..."}
          </h1>
        </div>
        <p className="text-sm text-ink-soft">
          {new Date().toLocaleDateString("es-CL", {
            weekday: "long",
            day: "numeric",
            month: "long",
          })}
        </p>
      </div>
    </header>
  );
}
