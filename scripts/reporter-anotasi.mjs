// Reporter node:test tambahan: kegagalan uji ditulis sebagai anotasi GitHub Actions.
export default async function* anotasi(sumber) {
  for await (const e of sumber) {
    if (e.type !== 'test:fail') continue;
    const err = e.data.details && e.data.details.error;
    const pesan = String((err && (err.cause && err.cause.message || err.message)) || 'gagal').replace(/\r?\n/g, ' ').slice(0, 900);
    yield `::error title=Uji gagal: ${e.data.name.replace(/[:,]/g, ' ')}::${pesan}\n`;
  }
}
