type Props = { rating: number; onDismiss: () => void };

export function NewAlertToast({ rating, onDismiss }: Props) {
  return (
    <div className="fixed top-6 right-6 z-50 toast-enter">
      <div className="bg-alert text-beige-card rounded-xl shadow-card px-5 py-4 flex items-center gap-4 min-w-[280px]">
        <div className="text-2xl">🚨</div>
        <div className="flex-1">
          <p className="font-semibold">Nueva alerta</p>
          <p className="text-sm opacity-90">Rating {rating}/5 recibido</p>
        </div>
        <button
          onClick={onDismiss}
          className="text-beige-card/80 hover:text-beige-card text-xl leading-none"
          aria-label="Cerrar"
        >
          ×
        </button>
      </div>
    </div>
  );
}
