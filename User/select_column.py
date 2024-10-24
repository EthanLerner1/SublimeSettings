import sublime
import sublime_plugin

class SelectColumnCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the current view (the current file being edited)
        view = self.view

        # Get the entire region of the file
        entire_file = sublime.Region(0, view.size())

        # Get the current selection (we assume there is only one selection)
        selection = view.sel()[0]

        # Get the starting and ending columns of the selection
        start_row, start_col = view.rowcol(selection.begin())
        end_row, end_col = view.rowcol(selection.end())

        # Calculate the width of the selection (in characters)
        selection_width = end_col - start_col

        # Create a list of regions to select the same width on all rows
        regions = []
        for row in range(view.rowcol(view.size())[0] + 1):
            # Calculate the starting and ending points for the new selection on each row
            start_point = view.text_point(row, start_col)
            end_point = view.text_point(row, start_col + selection_width)

            # Make sure the region doesn't exceed the line length (avoid errors on short lines)
            if end_point > view.line(start_point).end():
                end_point = view.line(start_point).end()

            regions.append(sublime.Region(start_point, end_point))

        # Clear any previous selection and set the new one
        view.sel().clear()
        view.sel().add_all(regions)

        # Scroll to the original caret position
        view.show_at_center(selection.begin())
