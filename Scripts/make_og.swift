// Immagine di anteprima social 1200×630: swift make_og.swift out.png icon.png font.ttf "Titolo" "Sottotitolo"
import AppKit
let a = CommandLine.arguments
CTFontManagerRegisterFontsForURL(URL(fileURLWithPath: a[3]) as CFURL, .process, nil)
let W = 1200, H = 630
let cg = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0,
                   space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(cgContext: cg, flipped: false)
let grad = NSGradient(colors: [NSColor(red: 1.0, green: 0.36, blue: 0.62, alpha: 1), NSColor(red: 0.93, green: 0.13, blue: 0.47, alpha: 1), NSColor(red: 0.74, green: 0.04, blue: 0.36, alpha: 1)])!
grad.draw(in: NSRect(x: 0, y: 0, width: W, height: H), angle: -35)
// crocini di cornice
NSColor.white.withAlphaComponent(0.55).setStroke()
let m: CGFloat = 44, l: CGFloat = 70
let p = NSBezierPath(); p.lineWidth = 6; p.lineCapStyle = .square
for (x, y, dx, dy) in [(m, m, 1.0, 1.0), (CGFloat(W) - m, m, -1.0, 1.0), (m, CGFloat(H) - m, 1.0, -1.0), (CGFloat(W) - m, CGFloat(H) - m, -1.0, -1.0)] {
    p.move(to: NSPoint(x: x + dx * l, y: y)); p.line(to: NSPoint(x: x, y: y)); p.line(to: NSPoint(x: x, y: y + dy * l))
}
p.stroke()
if let icon = NSImage(contentsOfFile: a[2]) { icon.draw(in: NSRect(x: 110, y: 190, width: 250, height: 250)) }
func font(_ s: CGFloat, _ w: NSFont.Weight) -> NSFont {
    let f = NSFont(name: "Bricolage Grotesque", size: s) ?? NSFont.systemFont(ofSize: s, weight: w)
    return w.rawValue > 0.3 ? NSFontManager.shared.convert(f, toHaveTrait: .boldFontMask) : f
}
a[4].draw(at: NSPoint(x: 410, y: 300), withAttributes: [.font: font(136, .heavy), .foregroundColor: NSColor.white])
a[5].draw(at: NSPoint(x: 416, y: 238), withAttributes: [.font: font(44, .semibold), .foregroundColor: NSColor.white.withAlphaComponent(0.92)])
NSGraphicsContext.restoreGraphicsState()
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, "public.png" as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg.makeImage()!, nil); CGImageDestinationFinalize(dest)
