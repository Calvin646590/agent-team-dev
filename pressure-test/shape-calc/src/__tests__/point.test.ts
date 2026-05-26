import { describe, it, expect } from "vitest";
import { Point } from "../geometry/point.js";

describe("Point", () => {
  it("constructor stores x and y correctly", () => {
    const p = new Point(3, 7);
    expect(p.x).toBe(3);
    expect(p.y).toBe(7);
  });

  it("constructor stores negative coordinates correctly", () => {
    const p = new Point(-5, -2);
    expect(p.x).toBe(-5);
    expect(p.y).toBe(-2);
  });

  it("distanceTo: same point has distance 0", () => {
    const p = new Point(4, 9);
    expect(p.distanceTo(p)).toBe(0);
  });

  it("distanceTo: 3-4-5 right triangle (distance from origin to (3,4) is 5)", () => {
    const origin = new Point(0, 0);
    const p = new Point(3, 4);
    expect(origin.distanceTo(p)).toBe(5);
  });

  it("distanceTo: symmetry (a.distanceTo(b) === b.distanceTo(a))", () => {
    const a = new Point(1, 2);
    const b = new Point(5, 6);
    expect(a.distanceTo(b)).toBe(b.distanceTo(a));
  });

  it("distanceTo: negative coordinates (Point(-1,-1) to Point(2,3))", () => {
    const a = new Point(-1, -1);
    const b = new Point(2, 3);
    // distance = sqrt((2-(-1))^2 + (3-(-1))^2) = sqrt(9+16) = sqrt(25) = 5
    expect(a.distanceTo(b)).toBeCloseTo(5, 10);
  });

  it("toString: format is 'Point(x, y)' for integer coordinates", () => {
    const p = new Point(3, 4);
    expect(p.toString()).toBe("Point(3, 4)");
  });

  it("toString: format is 'Point(x, y)' for floating point coordinates", () => {
    const p = new Point(1.5, 2.75);
    expect(p.toString()).toBe("Point(1.5, 2.75)");
  });
});
