"""
A set of utility functions to help create text visualizations.
"""

def draw_token(figure, axes, text, x, y, style, wordspacing, *args, **kwargs):
	"""
	Draw the token on the plot.

	:param figure: The figure that the component occupies.
				   This is used to get the figure renderer.
	:type figure: :class:`matplotlib.figure.Figure`
	:param axes: The axes (or subplot) where the component is plotted.
	:type axes: :class:`matplotlib.axes.Axes`
	:param text: The text token to draw.
	:type text: str
	:param x: The x-position of the token.
	:type x: int
	:param y: The y-position of the token.
	:type y: int
	:param style: The style information for the token.
	:type style: dict
	:param wordspacing: The space between words.
	:type wordspacing: float

	:return: The drawn text box.
	:rtype: :class:`matplotlib.text.Text`
	"""

	kwargs.update(style)
	"""
	Some styling are set specifically for the bbox.
	"""
	bbox_kwargs = { 'facecolor': 'None', 'edgecolor': 'None' }
	for arg in bbox_kwargs:
		if arg in kwargs:
			bbox_kwargs[arg] = kwargs.get(arg)
			del kwargs[arg]

	"""
	The bbox's padding is calculated in pixels.
	Therefore it is transformed from the provided axes coordinates to pixels.
	"""
	wordspacing_px = (axes.transData.transform((wordspacing, 0))[0] -
					  axes.transData.transform((0, 0))[0])
	text = axes.text(x, y, text,
					 bbox=dict(pad=wordspacing_px / 2., **bbox_kwargs),
					 *args, **kwargs)
	return text
