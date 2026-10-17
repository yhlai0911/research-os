// Adapted from the existing Claude Max collaboration in evidence/claude-code-followup.json.
// Review changes: preserve contrast, avoid borderWidth/layout animation, explicit return states.
const RO_AMBER = "#FFCE57";
const RO_MUTED = "#596479";

function evidenceFocus(tl, element, start, hold, scale, targetOffsetX, targetOffsetY) {
  const tx = -targetOffsetX * scale;
  const ty = -targetOffsetY * scale;
  tl.fromTo(element,
    {x: 0, y: 0, scale: 1, transformOrigin: "50% 50%"},
    {x: tx, y: ty, scale, duration: .9, ease: "power2.inOut", immediateRender: false}, start);
  tl.fromTo(element, {x: tx, y: ty, scale},
    {x: 0, y: 0, scale: 1, duration: .8, ease: "power2.inOut", immediateRender: false},
    start + .9 + hold);
  return tl;
}

function flowFrontier(tl, nodes, start, span) {
  const list = Array.from(nodes).slice(0, 6);
  const step = span / Math.max(list.length, 1);
  list.forEach((node, i) => {
    const rect = node.querySelector("rect");
    if (rect) tl.fromTo(rect, {stroke: RO_MUTED},
      {stroke: RO_AMBER, duration: Math.min(.5, step*.8), ease: "power1.out"}, start+i*step);
  });
  return tl;
}

function evidenceCompare(tl, beforeElement, afterElement, start, duration) {
  const d = Math.max(.4, duration);
  // .4 opacity in the raw proposal made the text too faint; retain .8 for readability.
  tl.fromTo(beforeElement, {opacity: 1},
    {opacity: .8, duration: d, ease: "power1.inOut", immediateRender: false}, start);
  tl.fromTo(afterElement, {opacity: .8},
    {opacity: 1, duration: d, ease: "power1.inOut", immediateRender: false}, start+d*.25);
  return tl;
}
