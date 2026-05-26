import { describe, it, expect } from "vitest";
import { Point } from "../geometry/point.js";
import { Line } from "../geometry/line.js";
import { perimeter } from "../geometry/perimeter.js";

describe("Line", () => {
  describe("length()", () => {
    it("horizontal line: Point(0,0) to Point(5,0) has length 5", () => {
      const line = new Line(new Point(0, 0), new Point(5, 0));
      expect(line.length()).toBe(5);
    });

    it("vertical line: Point(0,0) to Point(0,3) has length 3", () => {
      const line = new Line(new Point(0, 0), new Point(0, 3));
      expect(line.length()).toBe(3);
    });

    it("diagonal 3-4-5 triangle: Point(0,0) to Point(3,4) has length 5", () => {
      const line = new Line(new Point(0, 0), new Point(3, 4));
      expect(line.length()).toBeCloseTo(5, 10);
    });
  });

  describe("slope()", () => {
    it("horizontal line has slope 0", () => {
      const line = new Line(new Point(0, 0), new Point(5, 0));
      expect(line.slope()).toBe(0);
    });

    it("vertical line returns null", () => {
      const line = new Line(new Point(0, 0), new Point(0, 3));
      expect(line.slope()).toBeNull();
    });

    it("positive slope: Point(0,0) to Point(2,4) has slope 2", () => {
      const line = new Line(new Point(0, 0), new Point(2, 4));
      expect(line.slope()).toBeCloseTo(2, 10);
    });

    it("negative slope: Point(0,4) to Point(2,0) has slope -2", () => {
      const line = new Line(new Point(0, 4), new Point(2, 0));
      expect(line.slope()).toBeCloseTo(-2, 10);
    });
  });

  describe("toString()", () => {
    it("formats correctly as 'Line(Point(x1, y1), Point(x2, y2))'", () => {
      const line = new Line(new Point(1, 2), new Point(3, 4));
      expect(line.toString()).toBe("Line(Point(1, 2), Point(3, 4))");
    });
  });
});

describe("perimeter() with Line", () => {
  it("perimeter(line) equals line.length() for a horizontal line", () => {
    const line = new Line(new Point(0, 0), new Point(5, 0));
    expect(perimeter(line)).toBe(line.length());
  });

  it("perimeter(line) equals line.length() for a diagonal line", () => {
    const line = new Line(new Point(0, 0), new Point(3, 4));
    expect(perimeter(line)).toBeCloseTo(line.length(), 10);
  });
});
