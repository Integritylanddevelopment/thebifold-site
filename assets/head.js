/* Runs before first paint: decide whether the adults-only gate shows. */
(function () {
  var d = document.documentElement, ok = false;
  try { ok = localStorage.getItem('crapp:thebifold:opened') === '1' && localStorage.getItem('crapp:thebifold:mode') === 'adult'; } catch (e) { ok = false; }
  if (!ok) d.classList.add('gate-pending');
})();
