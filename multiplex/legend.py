"""
A legend contains a list of labels and their visual representation.
"""

import os
import sys

from matplotlib import lines

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from text.annotation import Annotation
import util

class Legend(object):
	"""
	The legend is made up of visual elements and a short label describing what they represent.

	:ivar drawable: The :class:`~drawable.Drawable` where the legend will be drawn.
	:vartype drawable: :class:`~drawable.Drawable`
	:ivar lines: The legend components, separated into lines.
				  Each component is a tuple of the visual representation and the associated label.
	:vartype lines: list of list of tuple
	"""

	def __init__(self, drawable):
		"""
		Create the legend.

		:param drawable: The :class:`~drawable.Drawable` where the legend will be drawn.
		:type drawable: :class:`~drawable.Drawable`
		"""

		self.lines = [ [ ] ]
		self.drawable = drawable

	def draw_line(self, label, label_style=None, *args, **kwargs):
		"""
		Draw a line legend for the given label.
		Any additional arguments and keyword arguments are provided to the plotting function.

		:param label: The text of the legend label.
		:type label: str
		:param label_style: The style of the label.
							If `None` is given, a default style is used.
		:type label_style: None or dict

		:return: A tuple made up of the function return value and the drawn label.
		:rtype: tuple
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		"""
		Get the offset for the new legend.
		Then, draw the line first and the annotation second.
		"""
		offset = self._get_offset(transform=axis.transAxes)
		linespacing = util.get_linespacing(figure, axis, transform=axis.transAxes)

		line = lines.Line2D([ offset, offset + 0.025 ], [ 1 + linespacing / 2. ] * 2,
							transform=axis.transAxes, *args, **kwargs)
		line.set_clip_on(False)
		axis.add_line(line)

		# TODO: Load the default style.
		label_style = label_style or { }
		line_offset = util.get_bb(figure, axis, line, transform=axis.transAxes).x1 + 0.00625
		annotation = self.draw_annotation(label, line_offset, 1, **label_style)
		if annotation.get_virtual_bb(transform=axis.transAxes).x1 > 1:
			self._newline(line, annotation, linespacing)
		else:
			self.lines[-1].append((line, annotation))

		return (line, annotation)

	def draw_annotation(self, label, x, y, va='bottom', *args, **kwargs):
		"""
		Get the annotation for the legend.
		The arguments and keyword arguments are passed on to the :meth:`~text.annotation.Annotation.draw` function.

		:param label: The text of the legend label.
		:type label: str
		:param x: The starting x-coordinate of the annotation.
		:type x: float
		:param y: The y-coordinate of the annotation.
		:type y: float
		:param va: The vertical alignment, can be one of `top`, `center` or `bottom`.
				   If the vertical alignment is `top`, the given y-coordinate becomes the highest point of the annotation.
				   If the vertical alignment is `center`, the given y-coordinate becomes the center point of the annotation.
				   If the vertical alignment is `bottom`, the given y-coordinate becomes the lowest point of the annotation.
		:type va: str

		:return: The drawn annotation.
		:rtype: :class:`~text.annotation.Annotation`
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		annotation = Annotation(self.drawable)
		annotation.draw(label, (x, 1), y, va=va, transform=axis.transAxes, **kwargs)
		return annotation

	def _get_offset(self, pad=0.025, transform=None):
		"""
		Get the x-coordinate offset for the next legend.

		:param pad: The padding to add to the offset.
					This padding is not added if there are no legends in the line.
		:type pad: float
		:param transform: The bounding box transformation.
						  If `None` is given, the data transformation is used.
		:type transform: None or :class:`matplotlib.transforms.TransformNode`

		:return: The x-coordinate offset for the next legend.
		:rtype: float
		"""

		if self.lines:
			last = self.lines[-1]
			if last:
				(visual, annotation) = last[-1]
				return annotation.get_virtual_bb(transform).x1 + pad

		return 0

	def _newline(self, visual, annotation, linespacing, va='center'):
		"""
		Create a new line with the given legend.

		:param visual: The visual of the legend.
		:type visual: object
		:param annotation: The drawn annotation.
		:type annotation: :class:`~text.annotation.Annotation`
		:param linespacing: The space between lines.
		:type linespacing: float
		:param va: The vertical alignment, can be one of `top`, `center` or `bottom`.
				   If the vertical alignment is `top`, the given y-coordinate becomes the highest point of the annotation.
				   If the vertical alignment is `center`, the given y-coordinate becomes the center point of the annotation.
				   If the vertical alignment is `bottom`, the given y-coordinate becomes the lowest point of the annotation.
		:type va: str
		"""

		figure = self.drawable.figure
		axis = self.drawable.axis

		"""
		Go through each line and move all of its components one line up.
		"""
		for line in self.lines:
			for push_visual, push_annotation in line:
				"""
				The lines can be pushed up by the height of the line.
				"""
				bb = util.get_bb(figure, axis, push_visual, transform=axis.transAxes)
				push_visual.set_ydata([ bb.y0 + linespacing ] * 2)

				"""
				The annotations are moved differently depending on the vertical alignment.
				If the vertical alignment is `top`, the annotation is moved from the top.
				If the vertical alignment is `center`, the annotation is moved from the center.
				If the vertical alignment is `bottom`, the annotation is moved from the bottom.
				"""
				bb = push_annotation.get_virtual_bb(transform=axis.transAxes)
				if va == 'top':
					y = bb.y1
				elif va == 'center':
					y = (bb.y0 + bb.y1) / 2.
				elif va == 'bottom':
					y = bb.y0

				push_annotation.set_position((bb.x0, y + linespacing), va=va, transform=axis.transAxes)

		"""
		Move the visual and the annotation to the start of the line.
		Finally, create a new line container.
		"""
		visualbb = util.get_bb(figure, axis, visual, transform=axis.transAxes)
		visual.set_xdata([ 0, 0.025 ])
		annotationbb = annotation.get_virtual_bb(transform=axis.transAxes)
		annotation.set_position((visualbb.width + 0.00625, 1), va=va, transform=axis.transAxes)
		self.lines.append( [ (visual, annotation) ] )