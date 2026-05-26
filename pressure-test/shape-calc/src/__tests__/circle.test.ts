import { describe, it, expect } from "vitest";
import { Point } from "../geometry/point.js";
import { Circle } from "../geometry/circle.js";
import { area } from "../geometry/area.js";
import { perimeter } from "../geometry/perimeter.js";

describe("Circle", () => {
  const center = new Point(0, 0);
  const radius = 5;
  const circle = new Circle(center, radius);

  it("area: π * r²", () => {
    expect(circle.area()).toBeCloseTo(Math.PI * radius * radius, 10);
  });

  it("area: π * r² for radius 1", () => {
    const unit = new Circle(new Point(0, 0), 1);
    expect(unit.area()).toBeCloseTo(Math.PI, 10);
  });

  it("perimeter: 2 * π * r", () => {
    expect(circle.perimeter()).toBeCloseTo(2 * Math.PI * radius, 10);
  });

  it("perimeter: 2 * π * r for radius 3", () => {
    const c = new Circle(new Point(1, 1), 3);
    expect(c.perimeter()).toBeCloseTo(2 * Math.PI * 3, 10);
  });

  it("contains: center point is inside", () => {
    expect(circle.contains(center)).toBe(true);
  });

  it("contains: point strictly inside the circle", () => {
    const inside = new Point(3, 0);
    expect(circle.contains(inside)).toBe(true);
  });

  it("contains: boundary point (exactly on the circle) is inside", () => {
    // Point at (5, 0) is exactly on the boundary of circle with center (0,0) and radius 5
    const boundary = new Point(5, 0);
    expect(circle.contains(boundary)).toBe(true);
  });

  it("contains: point outside the circle", () => {
    const outside = new Point(6, 0);
    expect(circle.contains(outside)).toBe(false);
  });

  it("contains: diagonal point outside", () => {
    // distance from (0,0) to (4,4) = sqrt(32) ≈ 5.66 > 5
    const outside = new Point(4, 4);
    expect(circle.contains(outside)).toBe(false);
  });

  it("negative radius throws Error('radius must be positive')", () => {
    expect(() => new Circle(new Point(0, 0), -1)).toThrow("radius must be positive");
  });

  it("zero radius throws Error", () => {
    expect(() => new Circle(new Point(0, 0), 0)).toThrow();
  });

  it("toString: correct format", () => {
    const c = new Circle(new Point(1, 2), 3);
    expect(c.toString()).toBe("Circle(Point(1, 2), 3)");
  });

  it("toString: format with center at origin", () => {
    expect(circle.toString()).toBe("Circle(Point(0, 0), 5)");
  });
});

describe("area/perimeter functions - Circle", () => {
  const center = new Point(2, 3);
  const radius = 7;
  const circle = new Circle(center, radius);

  it("area(circle) equals circle.area()", () => {
    expect(area(circle)).toBeCloseTo(circle.area(), 10);
  });

  it("perimeter(circle) equals circle.perimeter()", () => {
    expect(perimeter(circle)).toBeCloseTo(circle.perimeter(), 10);
  });
});
