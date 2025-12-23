---
title: "Create and Modify PDF Files in Python"
source: "https://realpython.com/creating-modifying-pdf/"
author:
  - "[[Real Python]]"
published: 2025-01-19
created: 2025-12-18
description: "In this tutorial, you'll explore the different ways of creating and modifying PDF files in Python. You'll learn how to read and extract text, merge and concatenate files, crop and rotate pages, encrypt and decrypt files, and even create PDFs from scratch."
tags:
  - "clippings"
---
# Create and Modify PDF Files in Python

**Source:** https://realpython.com/creating-modifying-pdf/

---

## 🧠 Summary
This Real Python tutorial explains how to create and modify PDF files in Python using two main libraries: pypdf (for reading and manipulating existing PDFs) and ReportLab (for generating PDFs from scratch). Key ideas and actionable points:

- Tools and install
  - pypdf: install with python -m pip install pypdf. Use PdfReader, PdfWriter, and (historically) PdfMerger.
  - ReportLab: install with python -m pip install reportlab. Main API: reportlab.pdfgen.canvas.Canvas.

- Reading & extracting text (pypdf)
  - PdfReader(path) gives .pages (list of PageObject) and .metadata.
  - PageObject.extract_text() returns page text; iterate pdf_reader.pages to extract whole-document text.
  - Example: save entire PDF text to a .txt file.

- Retrieving, writing, and splitting pages
  - PdfWriter creates new PDFs; add_blank_page() or add_page(existing_page). Use write(output_path) to save.
  - Extract a single page or slice pages to build a new PDF; PdfWriter.append_pages_from_reader(reader) copies all pages.

- Concatenation and merging
  - PdfMerger (note: deprecated in favor of PdfWriter.merge) can .append() (concatenate) or .merge(index, path) (insert). Useful for combining reports, inserting TOCs, etc.

- Rotating and cropping pages
  - PageObject.rotate(angle) and .rotation let you adjust page orientation programmatically.
  - RectangleObject (.mediabox) exposes coordinates and corner properties (.upper_left, .upper_right, etc.) so you can crop pages or split columns by changing those coordinates.

- Encrypting and decrypting
  - PdfWriter.encrypt(user_password, owner_password) adds password protection (pypdf currently uses RC4; AES support for encryption is limited).
  - PdfReader.decrypt(password) unlocks a protected file; .decrypt() returns enum indicating success/owner vs user password.

- Creating PDFs from scratch (ReportLab)
  - Canvas(filename, pagesize=...) to draw text, shapes, images. Use drawString(), setFont(), setFillColor(), save().
  - Use reportlab.lib.units (inch, cm) and reportlab.lib.pagesizes (LETTER, A4) to set sizes. Default fonts: Courier, Helvetica, Times-Roman; can set size and color.
  - ReportLab supports more advanced features (tables, forms, graphics) beyond the basics shown.

- Practical notes & gotchas
  - Page indices are 0-based; PDF page numbers may be 1-based (mind off-by-one when reasoning about odd/even pages).
  - .rotation may not reflect visual rotation for some scanned PDFs; manual inspection sometimes required.
  - pypdf has had breaking API changes historically (PyPDF2 → pypdf); check versions and docs.

- Learning aids
  - The article includes ready-to-run code examples and small exercises (extract first page text, concatenate PDFs, crop/split pages, encrypt/decrypt, create a simple PDF).

In short: use pypdf to read, extract, split, merge, rotate/crop, and (limited) encrypt/decrypt existing PDFs; use ReportLab Canvas to generate custom PDFs with precise layout, fonts, and graphics.

---

## 📝 Full Content
![Creating and Modifying PDF Files in Python](https://realpython.com/cdn-cgi/image/width=480,format=auto/https://files.realpython.com/media/UPDATE-Create-and-Modify-PDF-Files-in-Python_Watermarked.2d721de871c6.jpg)

Creating and Modifying PDF Files in Python

Creating and modifying PDF files in Python is straightforward with libraries like `pypdf` and ReportLab. You can read, manipulate, and create PDF files using these tools. `pypdf` lets you extract text, split, merge, rotate, crop, encrypt, and decrypt PDFs. ReportLab enables you to create new PDFs from scratch, allowing customization with fonts and page sizes.

**By the end of this tutorial, you’ll understand that:**

- You can **read and modify existing PDF files** using `pypdf` in Python.
- You can **create new PDF files** from scratch with the ReportLab library.
- Methods to **encrypt and decrypt a PDF file** with a password are available in `pypdf`.
- **Concatenating and merging multiple PDF files** can be done using `pypdf`.
- You can add **custom fonts** to a PDF using ReportLab.
- Python can create **interactive PDFs with forms** using ReportLab.

To follow along with this tutorial, you should download and extract to your home folder the materials used in the examples. To do this, click the link below:

## Extracting Text From PDF Files With pypdf

In this section, you’ll learn how to read PDF files and extract their text using the [`pypdf`](https://pypi.org/project/pypdf/) library. Before you can do that, though, you need to install it with [`pip`](https://realpython.com/what-is-pip/):

With this command, you download and install the latest version of `pypdf` from the Python package index ([PyPI](https://realpython.com/pypi-publish-python-package/)). To verify the installation, go ahead and run the following command in your [terminal](https://realpython.com/terminal-commands/):

Pay particular attention to the version information. At the time of publication for this tutorial, the latest version of `pypdf` was `3.8.1`. This library has gotten plenty of updates lately, and cool new features are added quite frequently. Most importantly, you’ll find many breaking changes in the library’s API if you compare it with its predecessor library [`PyPDF2`](https://pypdf.readthedocs.io/en/stable/meta/history.html#pypdf2-is-born-2011-2016).

Before diving into working with PDF files, you must know that this tutorial is adapted from the chapter “Creating and Modifying PDF Files” in [*Python Basics: A Practical Introduction to Python 3*](https://realpython.com/products/python-basics-book/).

The book uses Python’s built-in [IDLE](https://realpython.com/python-idle/) editor to create and edit Python files and interact with the Python shell, so you’ll find occasional references to IDLE throughout this tutorial. However, you should have no problems running the example code from the [editor](https://realpython.com/python-ides-code-editors-guide/) and environment of your choice.

[Remove ads](https://realpython.com/account/join/)

### Reading PDF Files With PdfReader

To kick things off, you’ll open a PDF file and read some information about it. You’ll use the `Pride_and_Prejudice.pdf` file provided in the downloadable resources for this tutorial.

Open IDLE’s interactive window and [import](https://realpython.com/python-import/) the `PdfReader` class from `pypdf`:

To create a new instance of the `PdfReader` class, you’ll need to provide the [path](https://realpython.com/read-write-files-python/#file-paths) to the PDF file that you want to open. You can do that using the [`pathlib`](https://realpython.com/python-pathlib/) module:

The `pdf_path` [variable](https://realpython.com/python-variables/) now contains the path to a PDF version of Jane Austen’s *Pride and Prejudice*.

Now create the `PdfReader` instance by calling the class’s [constructor](https://realpython.com/python-class-constructor/) with the path to your PDF file as an argument:

If you’ve been following along in *Python Basics*, then you’ll remember from Chapter 12, “File Input and Output,” that [all open files should be closed](https://realpython.com/why-close-file-python/) before a program terminates. The `PdfReader` object does all of this for you, so you don’t need to worry about opening or closing the PDF file!

Now that you’ve created a `PdfReader` instance, you can use it to gather information about the PDF file. For example, to get the number of pages contained in the PDF file, you can use the built-in [`len()`](https://realpython.com/len-python-function/) function like in the code below:

The `.pages` attribute holds a read-only list of [`PageObject`](https://pypdf.readthedocs.io/en/stable/modules/PageObject.html#the-pageobject-class) objects. Each object in the list represents a page in the underlying PDF file. So, `len()` gives you the number of pages in the document.

You can also access some document information using the `.metadata` attribute:

The object stored in `.metadata` looks like a [dictionary](https://realpython.com/python-dicts/) but isn’t the same thing. You can access each item in `.metadata` as an [attribute](https://realpython.com/python3-object-oriented-programming/#class-and-instance-attributes). For example, to get the title, use the `.title` attribute:

The `.metadata` object contains the PDF’s **metadata**, which is set when the file is first created. The `PdfReader` class provides all the necessary methods and attributes that you need to access data in a PDF file. In the following sections, you’ll explore what you can do with a PDF file and how you can do it!

### Extracting Text From a Page

In `pypdf`, the `PageObject` class represents the pages of a PDF file. You use `PageObject` instances to interact with pages in a PDF file. You don’t need to create your own `PageObject` instances directly. Instead, you can access them through the `PdfReader` object’s `.pages` attribute as you saw before.

If you need to extract text from a PDF page, then you need to run the following steps:

1. Get a `PageObject` with `PdfReader.page[page_index]`.
2. Extract the text as a string with the `PageObject` instance’s `.extract_text()` method.

`Pride_and_Prejudice.pdf` has `234` pages. Each page has an index between `0` and `233`. You can get the `PageObject` representing a specific page by using that index:

The indexing operation in the first line of the code above returns a `PageObject` instance, as you can conclude from the output of `type()`. Now you can use this instance to extract the page’s text using the `.extract_text()` method like in the example below:

```
>>> print(first_page.extract_text())

The Project Gutenberg EBook of Pride and Prejudice, by Jane Austen

This eBook is for the use of anyone anywhere at no cost and with
almost no restrictions whatsoever.  You may copy it, give it away or
re-use it under the terms of the Project Gutenberg License included
with this eBook or online at www.gutenberg.org

Title: Pride and Prejudice

Author: Jane Austen

Release Date: August 26, 2008 [EBook #1342]
[Last updated: August 11, 2011]

Language: English

Character set encoding: ASCII

*** START OF THIS PROJECT GUTENBERG EBOOK PRIDE AND PREJUDICE ***

Produced by Anonymous Volunteers, and David Widger

PRIDE AND PREJUDICE

By Jane Austen

Contents
```

Note that the output displayed above has been formatted to fit better on this page. The output that you see on your computer may be formatted differently.

Every `PdfReader` object has a `.pages` attribute that you can use to iterate over all of the pages in the PDF file in order. For example, the following [`for` loop](https://realpython.com/python-for-loop/) prints the text from every page in the *Pride and Prejudice* PDF:

If you run this code, then you’ll get a lot of text on your screen. In the following section, you’ll combine everything that you’ve learned by writing a small program that extracts all of the text from the `Pride_and_Prejudice.pdf` file and saves it to a `.txt` file.

[Remove ads](https://realpython.com/account/join/)

### Putting It All Together

Open a new editor window in IDLE, create a new `.py` file called `save_to_txt.py`, and type in the following code:

Here’s a breakdown of how this code works like by line:

- **Line 1** imports `Path` from `pathlib`, while line 5 imports `PdfReader`.
- **Lines 5 to 10** define a `Path` object containing the path to your target PDF file.
- **Line 12** assigns a new `PdfReader` instance to the `pdf_reader` [variable](https://realpython.com/python-variables/).
- **Line 13** creates a `Path` object that points to the output `.txt` file.
- **Lines 14 to 17** create a list where you’ll store the content that you’ll save to the `.txt` file. Initially, this list only contains the PDF title and the number of pages.
- **Lines 19 and 20** define a `for` loop that iterates over the PDF pages, extracts their content as strings, and [appends](https://realpython.com/python-append/) these strings to `content`.
- **Line 22** [concatenates](https://realpython.com/python-string-concatenation/) all the strings in `content` using the `.join()` method and a newline (`\n`) character as a separator. Finally, it writes the concatenated text into `txt_file` by taking advantage of `.write_text()` from `Path`.

When you save and run the program, it’ll create a new file in your home directory called `Pride_and_Prejudice.txt` containing the full text of the `Pride_and_Prejudice.pdf` document. Open it up and check it out!

### Checking Your Understanding

Expand the block below to check your understanding of all the concepts and tools that you’ve learned about in the previous sections:

In the `practice_files/` folder in the companion repository for this article, there’s a file called `zen.pdf`. Create a `PdfReader` instance that reads the PDF and uses it to print the text from the first page.

You can expand the block below to see a solution:

Set up the path to the PDF file:

Now you can create the `PdfReader` instance:

Now use run the following code to get the first page:

Remember, pages are indexed starting with `0`!

Then use `.extract_text()` to extract the page’s text:

Finally, [print](https://realpython.com/python-print/) the text to your screen:

```
print(text)
```

You’ll see the first page’s content on your screen.

When you’re ready, you can move on to the next section, where you’ll learn to extract pages from an existing PDF file.

## Retrieving Pages From a PDF File With pypdf

In the previous section, you learned how to extract all of the text from a PDF file and save it to a `.txt` file. In this section, you’ll learn how to retrieve a page or range of pages from an existing PDF and save them to a new PDF. To create a new PDF file, you’ll use the [`PdfWriter`](https://pypdf.readthedocs.io/en/stable/modules/PdfWriter.html) class from `pypdf`.

### Writing to PDF Files With PdfWriter

The `PdfWriter` class creates new PDF files. In IDLE’s interactive window, import the `PdfWriter` class and create a new instance called `pdf_writer`:

`PdfWriter` objects are like blank PDF files. You need to add some pages to them before you can save them to a file.

Go ahead and add a blank page to `pdf_writer`:

The `width` and `height` arguments are required. They determine the dimensions of the page in **user space units**. One of these units is equal to 1/72 of an inch, so the above code adds an [A4](https://en.wikipedia.org/wiki/ISO_216#A_series) blank page to `pdf_writer`.

The [`.add_blank_page()`](https://pypdf.readthedocs.io/en/stable/modules/PdfWriter.html#pypdf.PdfWriter.add_blank_page) method [returns](https://realpython.com/python-return-statement/) a new `PageObject` instance representing the page that you added to `PdfWriter`:

In this example, you’ve assigned the `PageObject` instance returned by `.add_blank_page()` to the `page` variable, but in practice, you don’t usually need to do this. That is, you usually call `.add_blank_page()` without assigning the return value to anything:

To write the contents of `pdf_writer` to a PDF file, pass a file object in binary write mode to `pdf_writer.write()`:

This creates a new file in your current working directory called `blank.pdf`. If you open the file with a PDF reader, such as Adobe Acrobat, then you’ll see a document with a single blank page with an A4 dimension.

`PdfWriter` objects can write to new PDF files, but they can’t create new content from scratch, other than blank pages. This might seem like a big problem, but in many situations, you don’t need to create new content. Often, you’ll work with pages extracted from PDF files that you’ve opened with the `PdfReader` class.

In the example above, you followed three steps to create a new PDF file using `pypdf`:

1. Create a `PdfWriter` instance.
2. Add one or more pages to the `PdfWriter` instance, using either `.add_blank_page()` or [`.add_page()`](https://pypdf.readthedocs.io/en/stable/modules/PdfWriter.html#pypdf.PdfWriter.add_page).
3. Write to a file using `PdfWriter.write()`.

You’ll see this pattern over and over as you learn various ways to add pages to a `PdfWriter` instance.

[Remove ads](https://realpython.com/account/join/)

### Extracting a Single Page From a PDF

In this section, you’ll revisit the *Pride and Prejudice* PDF file that you worked with in previous sections. You’ll open the PDF file, extract the first page, and create a new PDF file containing just the extracted page.

Open IDLE’s interactive window and import `PdfReader` and `PdfWriter` from `pypdf` as well as the `Path` class from the `pathlib` module:

Now open the `Pride_and_Prejudice.pdf` file with a `PdfReader` instance:

Go ahead and grab the index `0` from the `.pages` attribute to get a `PageObject` representing the first page of the PDF file:

Now create a `PdfWriter` instance and add `first_page` to it with `.add_page()`, as in the code below:

The `.add_page()` method adds a page to the list of pages in the `output_pdf` object, just like `.add_blank_page()`. The difference is that the former requires an existing `PageObject`, while the latter creates a new blank page.

Now write the contents of `output_pdf` to a new file:

You now have a new PDF file saved in your current working directory called `first_page.pdf`. This file contains the cover page of the `Pride_and_Prejudice.pdf` file. Pretty neat!

### Extracting Multiple Pages From a PDF

You can also extract multiple pages from a PDF file. For example, you can extract the first chapter from `Pride_and_Prejudice.pdf` and save it to a new PDF.

If you open `Pride_and_Prejudice.pdf` with a PDF viewer, then you can see that the second, third, and fourth pages of the PDF contain the first chapter. Since pages are indexed starting with `0`, you’ll need to extract the pages at the indices `1`, `2`, and `3`.

You can set everything up by importing the classes that you need and opening the PDF file:

Your goal is to extract the pages at indices `1`, `2`, and `3`, add these to a new `PdfWriter` instance, and then write them to a new PDF file.

One way to do this is to loop over the range of numbers starting at `1` and ending at `3`, extracting the page at each step of the loop and adding it to the `PdfWriter` instance:

The loop iterates over the pages `1`, `2`, and `3` by [slicing](https://realpython.com/python-strings/#string-slicing) the `.pages` attribute. At each step in the loop, the current page is added to the `output_pdf` object using `.add_page()`.

Now `output_pdf` has three pages, which you can check with the following code:

Finally, you can write the extracted pages to a new PDF file:

Now you can open the `chapter1.pdf` file in your current working directory to read just the first chapter of *Pride and Prejudice*.

Sometimes you need to extract every page from a PDF. You can use the methods illustrated above to do this, but `pypdf` provides a shortcut. `PdfWriter` instances have the [`.append_pages_from_reader()`](https://pypdf.readthedocs.io/en/stable/modules/PdfWriter.html#pypdf.PdfWriter.append_pages_from_reader) method, which you can use to append pages from a `PdfReader` instance.

To use `.append_pages_from_reader()`, pass a `PdfReader` instance to the method’s `reader` parameter. For example, the following code copies every page from the *Pride and Prejudice* PDF to a `PdfWriter` instance:

Your `pdf_writer` object now contains every page in `input_pdf`! Save the content of `pdf_writer` to a PDF file with `.write()` and open it with the resulting PDF file in a viewer.

[Remove ads](https://realpython.com/account/join/)

### Checking Your Understanding

Go ahead and expand the block below to check your understanding of all the concepts and tools that you’ve learned about in the previous sections:

Extract the last page from the `Pride_and_Prejudice.pdf` file and save it to a new file called `last_page.pdf` in your home directory.

You can expand the block below to see a solution:

Set up the path to the `Pride_and_Prejudice.pdf` file:

Now you can create the `PdfReader` instance:

Next, you can use the `.pages` attribute to get all the pages in the input PDF file. To get the last page, you can use the index `-1`:

Now you can create a `PdfWriter` instance and add the last page to it:

Finally, write the contents of `output_pdf` to the file `last_page.pdf` in your home directory:

Go ahead and open the `last_page.pdf` file in your PDF viewer to check that everything worked okay.

When you’re ready, you can move on to the next section.

## Concatenating and Merging PDF Files With pypdf

Concatenating and merging several PDF files into a single file are two common tasks when you’re working with PDF files.

When you **concatenate** two or more PDF files, you join the files one after another into a single document. For example, a company may concatenate several daily reports into one monthly report at the end of a month.

**Merging** two PDF files also joins them into a single file, but instead of attaching the second PDF to the end of the first, merging inserts the file after a specific page in the first PDF. Then it pushes all of the first PDF’s pages after the insertion point to the end of the second PDF.

In this section, you’ll learn how to concatenate and merge PDF files using the `pypdf` library and its `PdfMerger` class.

### Merging PDF Files With PdfMerger

The `PdfMerger` class is a lot like the `PdfWriter` class that you learned about in the previous section. You can use both classes to write PDF files. In both cases, you add pages to instances of the class and then write them to a file.

The main difference between the two is that `PdfWriter` can only append, or concatenate, pages to the end of the list of pages already contained in the writer. Conversely, `PdfMerger` can insert, or merge, pages at any location.

Go ahead and create your first `PdfMerger` instance. In IDLE’s interactive window, type the following code to import the `PdfMerger` class and create a new instance:

`PdfMerger` objects are empty when you first instantiate them. You’ll need to add some pages to your object before you can do anything with it.

There are a couple of ways to add pages to a `PdfMerger` object, and you’ll choose one based on what you need to accomplish:

- `.append()` concatenates every page in an existing PDF document to the end of the pages currently in `PdfMerger`.
- `.merge()` inserts all of the pages in an existing PDF document after a specific page in `PdfMerger`.

In the following sections, you’ll look at both methods, starting with `.append()`.

[Remove ads](https://realpython.com/account/join/)

### Concatenating PDFs With.append()

The `practice_files/` folder in the downloadable materials for this tutorial has a subdirectory called `expense_reports` that contains three expense reports for an employee named Peter Python.

Peter needs to concatenate these three PDFs and submit them to his employer as a single PDF file for reimbursement of some work-related expenses.

You can start by using the `pathlib` module to get a list of `Path` objects for each of the three expense reports in the `expense_reports/` folder:

After you import the `Path` class, you need to build the path to the `expense_reports/` directory. Note that you may need to alter the code above to get the correct path on your computer.

Once you have the path to the `expense_reports/` directory assigned to the `reports_dir` variable, you can use `.glob()` to get an iterable of paths to PDF files in the directory.

Take a look at what’s in the directory:

The names of the three files are listed, but they aren’t in order. Furthermore, the order of the files that you see in the output on your computer may not match the output shown here.

In general, the order of paths that [`.glob()`](https://realpython.com/get-all-files-in-directory-python/#using-a-python-glob-pattern-for-conditional-listing) returns isn’t guaranteed, so you’ll need to order them yourself. You can do this by creating a list using the built-in [`.sorted()`](https://realpython.com/python-sort/#ordering-values-with-sorted) function:

Remember that `.sorted()` takes an iterable and returns a list, so you need to assign the return value to a variable. The method will sort the list in `expense_reports` alphabetically by filename.

To confirm that the sorting worked, loop over `expense_reports` again and print out the filenames:

That looks good! They’re sorted as you need. Now you can proceed to concatenate the three PDF files into a single file. To do that, you’ll use `PdfMerger.append()`. This method takes the path to a PDF file. When you call `.append()`, you append all of the pages in the PDF file to the set of pages in the `PdfMerger` object.

To see this in action, go ahead and import the `PdfMerger` class and create a new instance:

Now loop over the paths in the sorted `expense_reports` list and append them to `pdf_merger`:

With all of the PDF files in the `expense_reports/` directory concatenated in the `pdf_merger` object, the last thing you need to do is to write everything to an output PDF file. `PdfMerger` instances have a `.write()` method that works just like `PdfWriter.write()`, so go ahead and use it:

You now have a PDF file in your current working directory called `expense_reports.pdf`. Open it up with a PDF viewer, and you’ll find all three expense reports together in the same PDF file.

[Remove ads](https://realpython.com/account/join/)

### Merging PDFs With.merge()

To merge two or more PDF files, use `PdfMerger.merge()`. This method is similar to `.append()`, except that you must specify where in the output PDF to insert all of the content from the PDF that you’re merging.

Take a look at an example. Goggle, Inc. prepared a quarterly report but forgot to include a table of contents. Peter Python noticed the mistake and quickly created a PDF with the missing table of contents. Now he needs to merge that PDF into the original report.

You can find both the report PDF and the table of contents PDF in the `quarterly_report/` subfolder of the `practice_files/` folder. The report is in a file called `report.pdf`, and the table of contents is in a file called `toc.pdf`.

In IDLE’s interactive window, import the `PdfMerger` class and create the `Path` objects for the `report.pdf` and `toc.pdf` files:

The first thing that you’ll do is append the report PDF to a new `PdfMerger` instance using `.append()`. So, go ahead and run the following code:

Now that `pdf_merger` has some pages in it, you can merge the table of contents PDF into it at the correct location. If you open the `report.pdf` file with a PDF viewer, then you’ll see that the first page of the report is a title page. The second is an introduction, and the remaining pages contain different report sections.

You want to insert the table of contents after the title page, just before the introduction page. Because PDF page indices start with `0` in `pypdf`, you need to insert the table of contents after the page at index `0` and before the page at index `1`.

To do that, call `pdf_merger.merge()` with two arguments:

1. The integer `1`, indicating the index of the page at which the table of contents should be inserted
2. The path to the PDF file containing the table of contents

Here’s what that looks like:

Every page in the table of contents PDF is inserted *before* the page at index `1`. Since the table of contents PDF is only one page, it gets inserted at index `1`. The page currently at index `1` then shifts to index `2`. The page currently at index `2` shifts to index `3`, and so on.

Now write the merged PDF to an output file:

You now have a `full_report.pdf` file in your current working directory. Open it up with a PDF viewer and check that the table of contents was inserted at the correct position.

Concatenating and merging PDFs are common operations. While the examples in this section are admittedly somewhat contrived, you can imagine how useful a program would be for merging thousands of PDFs or for automating routine tasks that would otherwise take a human lots of time to complete.

### Checking Your Understanding

Again, you can expand the block below to check your understanding of all the concepts and tools that you’ve learned about in the previous sections:

In the `practice_files/` folder in the companion repository for this article, there are two files called `merge1.pdf` and `merge2.pdf`.

Using a `PdfMerge` instance, concatenate the two files using `.append()`. Save the concatenated PDFs to a new file called `concatenated.pdf` in your computer’s home directory.

You can expand the block below to see a solution:

Set up the path to the PDF file:

Now you can create the `PdfMerger` instance:

Now loop over the paths in `pdf_paths` and append each file to `pdf_merger`:

Finally, write the contents of `pdf_merger` to a file called `concatenated.pdf` in your home directory:

Go ahead and open `concatenated.pdf` in your PDF viewer. You’ll have the content of `merge2.pdf` appended to the original content in `merge1.pdf`.

When you’re ready, you can move on to the next section.

[Remove ads](https://realpython.com/account/join/)

## Rotating and Cropping PDF Pages With pypdf

So far, you’ve learned how to extract text and pages from PDFs and how to concatenate and merge two or more PDF files. These are all common operations with PDF files, but `pypdf` has many other useful features.

In the following sections, you’ll learn how to rotate and crop pages in a PDF file.

### Rotating Pages With PageObject.rotate()

You’ll start by learning how to rotate pages. For this example, you’ll use the `ugly.pdf` file in the `practice_files/` folder. This file contains a lovely version of Hans Christian Andersen’s “The Ugly Duckling,” except that every odd-numbered page is rotated counterclockwise by ninety degrees.

To fix that, in a new IDLE interactive window, start by importing the `PdfReader` and `PdfWriter` classes from `pypdf`, as well as the `Path` class from the `pathlib` module:

Now create a `Path` object for the `ugly.pdf` file:

Finally, create new `PdfReader` and `PdfWriter` instances with the following code:

Your goal is to use `pdf_writer` to create a new PDF file in which all of the pages have the correct orientation. The even-numbered pages in the PDF are already properly oriented, but the odd-numbered pages are rotated counterclockwise by ninety degrees.

To correct the problem, you’ll use [`PageObject.rotate()`](https://pypdf.readthedocs.io/en/stable/modules/PageObject.html#pypdf._page.PageObject.rotate). This method rotates a page clockwise by a certain angle. For example, `.rotate(90)` rotates a PDF page clockwise by ninety degrees. Note that this argument only accepts values that are multiples of `90` degrees.

There are several ways you can go about rotating pages in the PDF. In this section, you’ll learn two different ways of doing it. Both of them rely on `.rotate()`, but they take different approaches to determine which pages get rotated.

The first technique is to loop over the indices of the pages in the PDF and check if each index corresponds to a page that needs to be rotated. If that’s the case, then you’ll call `.rotate()` to rotate the page and then add the page to `pdf_writer`.

Here’s how to do that:

Notice that the page gets rotated if the index is even. That might seem strange since the odd-numbered pages in the PDF are the ones that are rotated incorrectly. However, the page numbers in the PDF start with `1`, whereas the page indices start with `0`. That means odd-numbered PDF pages have even indices.

If that makes your head spin, don’t worry! Even after years of dealing with stuff like this, professional programmers still get tripped up by these sorts of things!

Now that you’ve rotated all the pages in the PDF, you can write the content of `pdf_writer` to a new file and check that everything worked:

You’ll now have a PDF file in your current working directory called `ugly_rotated.pdf`, with the pages from `ugly.pdf` all in the correct orientation.

The problem with this approach is that it depends on knowing ahead of time which pages need to be rotated. In a real-world scenario, it’s inefficient to go through an entire PDF taking note of which pages to rotate.

Luckily, you don’t need prior knowledge to determine which pages you need to rotate. Instead, you can access the page’s [`.rotation`](https://pypdf.readthedocs.io/en/stable/modules/PageObject.html#pypdf._page.PageObject.rotation) attribute. To illustrate this trick, go ahead and create a new `PdfReader` instance as usual:

You need to do this because you altered the pages in the old `PdfReader` instance by rotating them. So, by creating a new instance, you’re starting fresh.

`PageObject` instances have an attribute called `.rotation` that holds the current visual rotation angle of the page at hand. For example, you can get the angle for the first page of `pdf_reader` by doing the following:

This value of `-90` is consistent with the fact that the first page of `ugly.pdf` is rotated counterclockwise by ninety degrees.

Now if you look at `.rotation` for the second page in `pdf_reader`, then you’ll see that it has a value of `0`:

A `0` rotation value means that the page is normally oriented. So, the `.rotation` attribute allows you to check the current rotation of the pages in `ugly.pdf` and then rotate any pages that don’t have a rotation of `0`.

The first thing you need to do is reinitialize your `pdf_reader` and `pdf_writer` objects so that you get a fresh start:

Now write a loop that iterates over the pages in `pdf_reader.pages`, checks the value of `.rotation`, and rotates the page if that value is different from `0`:

This solution doesn’t rely on any prior knowledge of which pages you need to rotate. You check if a page’s rotation angle is different from `0`. If that’s the case, then you rotate the page by the same angle but with an inverted sign. Finally, you add the page to the PDF writer as usual.

To finish out the solution, write the contents of `pdf_writer` to a new file:

Now you can open `ugly_rotated2.pdf` in your current working directory and compare it to the `ugly_rotated.pdf` file that you generated earlier. They’ll look identical.

The value of `.rotation` may not always be what you expect. For example, if you scan a paper document with the page rotated ninety degrees counterclockwise, then the contents of the PDF will appear rotated. However, the `.rotation` attribute may have the value `0`.

This is one of many quirks that can make working with PDF files frustrating. Sometimes you’ll just need to open a PDF in a PDF viewer program and manually figure things out.

[Remove ads](https://realpython.com/account/join/)

### Cropping Pages With RectangleObject

Another common operation with PDFs is cropping pages. You might need to do this to split a single page into multiple pages or to extract just a small portion of a page, such as a signature or a figure.

For example, the `practice_files/` folder includes a file called `half_and_half.pdf`. This PDF contains a portion of Hans Christian Andersen’s “The Little Mermaid.” Each page in this PDF has two columns. You can split each page into two pages, one for each column.

To get started, import the `PdfReader` and `PdfWriter` classes from `pypdf` and the `Path` class from the `pathlib` module:

Now create a `Path` object for the `half_and_half.pdf` file:

Next, create a new `PdfReader` object and get the first page of the target PDF file:

To crop the page, you first need to know a little bit more about how pages are structured. `PageObject` instances like `first_page` have a [`.mediabox`](https://pypdf.readthedocs.io/en/stable/modules/PageObject.html#pypdf._page.PageObject.mediabox) attribute that represents a rectangular area defining the boundaries of the page.

You can use IDLE’s interactive window to explore `.mediabox` before using it to crop the page:

The `.mediabox` attribute holds a [`RectangleObject`](https://pypdf.readthedocs.io/en/stable/modules/RectangleObject.html#pypdf.generic.RectangleObject) instance. This object represents a rectangular area on the page.

The [list](https://realpython.com/python-lists-tuples/) `[0.0, 0.0, 792, 612]` in the output defines the rectangular area. The first two numbers are the `x` and `y` coordinates of the lower-left corner of the rectangle. The third and fourth numbers represent the width and height of the rectangle, respectively. The units of all of the values are *user space units*, which are equal to 1/72 of an inch, as you already learned.

In this example, the rectangular region with the lower-left corner at the origin has a width of 792 user space units, or 11 inches, and a height of 612 user space units, or 8.5 inches. Those are the dimensions of a standard letter-sized page in landscape orientation, which is used for the example PDF of “The Little Mermaid.” A letter-sized PDF page in portrait orientation would return the output `RectangleObject([0.0, 0.0, 612, 792])`.

`RectangleObject` has four attributes that return the coordinates of the rectangle’s corners: `.lower_left`, `.lower_right`, `.upper_left`, and `.upper_right`. Just like the width and height values, these coordinates are given in user space units.

You can use these four properties to get the coordinates of each corner of the `RectangleObject`:

Each property returns a [tuple](https://realpython.com/python-tuple/) containing the coordinates of the specified corner. You can access individual coordinates with square brackets, just like you would do with any other Python tuple:

You can alter the coordinates of `.mediabox` by assigning a new list to one of its properties:

When you change the `.upper_left` coordinates, the `.upper_right` attribute automatically adjusts to preserve a rectangular shape:

When you alter the coordinates of the `RectangleObject` returned by `.mediabox`, you effectively crop the page. The `first_page` object now contains only the information present within the boundaries of the resized `RectangleObject`.

Go ahead and write the cropped page to a new PDF file:

If you open `cropped_page.pdf` in your current working directory, then you’ll see that the top portion of the page has been removed.

How would you crop the page so that just the text on the left side of the page is visible? You would need to cut the horizontal dimensions of the page in half. You can achieve this by altering the `.upper_right` coordinates of the `.mediabox` object.

First, you need to get new `PdfReader` and `PdfWriter` objects since you’ve just altered the first page in `pdf_reader` and added it to `pdf_writer`:

Now get the first page of the PDF:

This time, you’ll work with a copy of the first page so that the page you just extracted stays intact. You can do that by importing the [`copy`](https://docs.python.org/3/library/copy.html#module-copy) module from Python’s standard library and using [`deepcopy()`](https://docs.python.org/3/library/copy.html#copy.deepcopy) to make a copy of the page:

Now you can alter `left_side` without changing the properties of `first_page`. That way, you can use `first_page` later to extract the text on the right side of the page.

Now you need to do a little bit of math. You already worked out that you need to move the upper right-hand corner of `.mediabox` to the top center of the page. To do that, you’ll create a new list with the first component equal to half the original value and assign it to the `.upper_right` property.

First, get the current coordinates of the upper-right corner of the `.mediabox` with the following [assignment](https://realpython.com/python-assignment-operator/):

Then create a new list whose first coordinate is half the value of the current coordinate and whose second coordinate is the same as the original:

Finally, assign the new coordinates to the `.upper_right` property:

You’ve now cropped the original page to contain only the text on the left side!

To extract the right side of the page next, first get a new copy of `first_page`:

Move the `.upper_left` corner instead of the `.upper_right` corner:

This assignment sets the upper-left corner to the same coordinates that you moved the upper-right corner to when extracting the left side of the page. So, `right_side.mediabox` is now a rectangle whose upper-left corner is at the top center of the page and whose upper-right corner is at the top right of the page.

Finally, add the `left_side` and `right_side` pages to `pdf_writer` and write them to a new PDF file:

Now open `cropped_pages.pdf` with a PDF reader. You should see a file with two pages, the first containing the text from the left-hand side of the original first page, and the second containing the text from the original right-hand side.

[Remove ads](https://realpython.com/account/join/)

### Checking Your Understanding

Expand the block below to check your understanding:

In the `practice_files/` folder in the companion repository for this tutorial, you’ll find a file called `split_and_rotate.pdf`.

In your computer’s home directory, create a new file called `rotated.pdf` that contains all of the pages from `split_and_rotate.pdf`, but with each one rotated counterclockwise by ninety degrees.

You can expand the block below to see a solution:

Set up the path to the PDF file:

Now you can create `PdfReader` and `PdfWriter` instances:

Loop over the pages in `pdf_reader`, rotate all of them by ninety degrees using `.rotateCounterClockwise()`, and add them to `pdf_writer`:

Finally, write the contents of `pdf_writer` to a file called `rotated.pdf` in your computer’s home directory:

Go ahead and open `rotated.pdf` in your favorite PDF viewer to check if everything worked as expected.

When you’re ready, you can move on to the next section.

## Encrypting and Decrypting PDF Files With pypdf

Sometimes PDF files are password protected. With the `pypdf` package, you can work with encrypted PDF files and also add password protection to existing PDFs.

To encrypt your documents with a password, you can use the [`.encrypt()`](https://pypdf.readthedocs.io/en/stable/modules/PdfWriter.html#pypdf.PdfWriter.encrypt) method on a `PdfWriter` object. Similarly, to decrypt an encrypted document, you can use the [`.decrypt()`](https://pypdf.readthedocs.io/en/stable/modules/PdfReader.html#pypdf.PdfReader.decrypt) method on a `PdfReader` object.

### Encrypting PDFs With PdfWriter.encrypt()

You can add password protection to a PDF file using the `.encrypt()` method of a `PdfWriter` instance. It has two main parameters:

1. **`user_password`** sets the user password. This argument allows for opening and reading the encrypted PDF file.
2. **`owner_password`** sets the owner password. This argument allows for opening and editing the PDF without any restrictions.

With `.encrypt()`, you can add a password to a PDF file. First, open `newsletter.pdf` in the `practice_files` directory:

Now create a new `PdfWriter` instance and add the pages from `pdf_reader` to it:

Next, add the password `"SuperSecret"` with `pdf_writer.encrypt()`:

When you set only `user_password`, the `owner_password` argument defaults to the same string. So, the above line of code sets both the user and owner passwords.

Finally, write the encrypted PDF to an output file in your home directory called `newsletter_protected.pdf`:

When you open the PDF file with a PDF viewer, you’ll be prompted to enter a password. Enter `"SuperSecret"` to open the PDF.

If you need to set a separate owner password for the PDF, then pass a second string to the `owner_password` parameter:

In this example, the user password is `"SuperSecret"`, and the owner password is `"ReallySuperSecret"`.

When you encrypt a PDF file with a password and attempt to open it, you must provide the password before you can view its contents. This protection extends to reading from the PDF in a Python program. Next, it’s time for you to learn how to decrypt PDF files with `pypdf`.

[Remove ads](https://realpython.com/account/join/)

### Decrypting PDFs With PdfReader.decrypt()

To decrypt an encrypted PDF file, use the `.decrypt()` method of a `PdfReader` instance. This method has a single parameter called `password` that you can use to provide the password for decryption. The privileges you have when opening the PDF depend on the argument that you passed to the `password` parameter.

Go ahead and open the encrypted `newsletter_protected.pdf` file that you created in the previous section and use `pypdf` to decrypt it.

First, create a new `PdfReader` instance with the path to the protected PDF file:

Before you decrypt the PDF file, check out what happens if you try to get the first page:

A `FileNotDecryptedError` exception is raised, informing you that the PDF file has not been decrypted.

Go ahead and decrypt the file using the password that you set in the previous section:

You’ll note that `.decrypt()` returns an [enumeration](https://realpython.com/python-enum/) object representing the success of the decryption. In this example, the method returns `<PasswordType.OWNER_PASSWORD: 2>`, which means that you’ve decrypted the PDF file with the owner password.

Once you’ve decrypted the file, you can access it contents as usual:

Now you can extract text and crop or rotate pages to your heart’s content!

### Checking Your Understanding

Now it’s time to check your understanding. Go ahead and expand the block below:

In the `practice_files/` folder in the companion repository for this article, there’s a file called `top_secret.pdf`.

Using `PdfWriter.encrypt()`, encrypt the file with the user password `Unguessable`. Save the encrypted file as `top_secret_encrypted.pdf` in your computer’s home directory.

You can expand the block below to see a solution:

Set up the path to the PDF file:

Now create `PdfReader` and `PdfWriter` instances:

You can append all of the pages from `pdf_reader` to `pdf_writer` using `.append_pages_from_reader()`:

```
pdf_writer.append_pages_from_reader(pdf_reader)
```

Now use `encrypt()` to set the user password to `"Unguessable"`:

```
pdf_writer.encrypt(user_password="Unguessable")
```

Finally, write the contents of `pdf_writer` to a file called `top_secret_encrypted.pdf` in your computer’s home directory:

Now, when you try to open `top_secret_encrypted.pdf` in your PDF viewer, it’ll prompt you for a password first.

When you’re ready, you can move on to the next section.

## Creating PDF Files With Python and ReportLab

The `pypdf` package is great for reading and modifying existing PDF files, but it has a major limitation. You can’t use it to create a new PDF file. In this section, you’ll use the [ReportLab](https://docs.reportlab.com/) library to generate PDF files from scratch.

ReportLab is a full-featured solution for creating PDFs. There’s a commercial version that costs money to use, but a limited-feature [open-source version](https://docs.reportlab.com/install/open_source_installation/) is also available.

### Installing ReportLab

To get started, you need to install `reportlab` with `pip`. Go ahead and run the following command:

You can verify the installation with `pip show`:

At the time of publication, the latest version of ReportLab was 4.0.0.

### Using the Canvas Class

The main interface for creating PDFs with ReportLab is the [`Canvas`](https://docs.reportlab.com/reportlab/userguide/ch2_graphics/#more-about-the-canvas) class, which you can find in the `reportlab.pdfgen.canvas` module.

Open a new IDLE interactive window and run the following line of code to import the `Canvas` class:

When you make a new `Canvas` instance, you need to provide a string with the filename of the PDF that you’re creating. Go ahead and create a new `Canvas` instance for the file `hello.pdf`:

You now have a `Canvas` instance that you’ve assigned to the variable name `canvas` and that’s associated with a file in your current working directory called `hello.pdf`. The file `hello.pdf` doesn’t exist yet, though.

Go ahead and add some text to the PDF file. To do that, use `.drawString()`, as in the code below:

The first two arguments to `.drawString()` determine the location where the text is written on the canvas. The first specifies the distance from the left edge of the canvas, and the second specifies the distance from the bottom edge.

The values passed to `.drawString()` are measured in user space points. Since a point equals 1/72 of an inch, the above code draws the string `"Hello, World!"` one inch from the left and one inch from the bottom of the page.

To save the PDF to a file, use the `.save()` method:

You now have a PDF file in your current working directory called `hello.pdf`. You can open it with a PDF reader and see the text `Hello, World` at the bottom of the page!

There are a few points to notice about the PDF file that you’ve just created:

1. The default page size is A4, which isn’t the same as the standard US letter page size.
2. The font family defaults to Helvetica with a size of 12 points.

You’re not stuck with these settings.

### Setting the Page Size

When you instantiate a `Canvas` object, you can define the page size with the `pagesize` [optional argument](https://realpython.com/python-optional-arguments/). This parameter accepts a tuple of [floating-point values](https://realpython.com/python-data-types/#floating-point-numbers) representing the width and height of the page in points.

For example, to set the page size to `8.5` inches wide by `11` inches tall, you’d create the following `Canvas` instance:

The tuple `(612.0, 792.0)` represents a letter-sized piece of paper because `8.5` times `72` is `612`, and `11` times `72` is `792`.

If doing the math to convert points to inches or centimeters isn’t your cup of tea, then you can use the `reportlab.lib.units` module to help you with the conversions. The `.units` module contains several helper objects, such as `inch` and `cm`, that simplify your conversions.

Go ahead and import the `inch` and `cm` objects from the `reportlab.lib.units` module:

Now you can inspect each object to see what they are:

Both `cm` and `inch` are [floating-point](https://realpython.com/python-numbers/#floating-point-numbers) values. They represent the number of points contained in each unit. Therefore, `cm` is `28.346456692913385` points, and `inch` is `72.0` points.

To use the units, multiply the unit name by the number of units that you want to convert to points. For example, here’s how to use `inch` to set the page size to `8.5` inches wide by `11` inches tall:

By passing a tuple to `pagesize`, you can create any size of page that you want. However, the ReportLab package has some standard built-in page sizes that are easier to work with.

The page sizes are located in the `reportlab.lib.pagesizes` module. For example, to set the page size to letter, you can import the `LETTER` object from the `pagesizes` module and pass it to the `pagesize` parameter when instantiating your `Canvas`:

If you inspect the `LETTER` object, then you’ll see that it’s a tuple of floats:

The `reportlab.lib.pagesize` module contains many standard page sizes. Here are a few of them with their dimensions:

| Page Size | Dimensions |
| --- | --- |
| `A4` | 8.27 in x 11.7 in |
| `LETTER` | 8.5 in x 11 in |
| `LEGAL` | 8.5 in x 14 in |
| `TABLOID` | 11 in x 17 in |

In addition to these, the module contains definitions for all of the [ISO 216 standard paper sizes](https://en.wikipedia.org/wiki/ISO_216).

### Setting Font Properties

You can also change the [font](https://docs.reportlab.com/rml/userguide/Chapter_3_Basic_Text_Operations/#using-fonts) and font settings when you write text to `Canvas`. To change the font and its size, you can use `.setFont()`. First, create a new `Canvas` instance with the filename `font-example.pdf` and a letter page size:

Then set the font to Times New Roman with a size of `18` points:

Finally, write the string `"Times New Roman (18 pt)"` to the canvas and save it:

With these settings, you’re writing the text one inch from the left side of the page and ten inches from the bottom. Open up `font-example.pdf` in your current working directory and check it out!

Three font families are available by default:

1. `"Courier"`
2. `"Helvetica"`
3. `"Times-Roman"`

Each font has bold and italic variants. Here’s a list of some font styles available in ReportLab:

- `"Courier"`
- `"Courier-Bold`
- `"Courier-BoldOblique"`
- `"Courier-Oblique"`
- `"Helvetica"`
- `"Helvetica-Bold"`
- `"Helvetica-BoldOblique"`
- `"Helvetica-Oblique"`
- `"Times-Bold"`
- `"Times-BoldItalic`
- `"Times-Italic"`
- `"Times-Roman"`

You can also set the font color using `.setFillColor()`. In the following example, you create a PDF file with blue text named `font-colors.pdf`:

Here, you import `blue` from the `reportlab.lib.colors` module. This module contains several common colors. You can find a full list of colors in the [ReportLab source code](https://realpython.com/pybasics-reportlab-source).

The examples in this section highlight the basics of working with the `Canvas` class. But you’ve only scratched the surface. With ReportLab, you can create tables, forms, and even high-quality graphics from scratch!

The [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf) contains a plethora of examples of how to generate PDF documents from scratch. It’s a great place to start if you’re interested in learning more about creating PDFs with Python.

### Checking Your Understanding

Expand the block below to check your understanding of how to create and customize PDF files from scratch:

Create a PDF in your computer’s home directory called `realpython.pdf` with letter-sized pages that contain the text `"Hello, Real Python!"` placed two inches from the left edge and eight inches from the bottom edge of the page.

You can expand the block below to see a solution:

Set up the `Canvas` instance with letter-sized pages:

Now draw the string `"Hello, Real Python!"` two inches from the left and eight inches from the bottom:

Finally, save `canvas` to write the PDF file:

```
canvas.save()
```

Now go ahead and open `realpython.pdf` on your PDF viewer to check if everything worked okay.

## Conclusion

You’ve learned the basics of how to work with existing PDF files using the `pypdf` library, including how to read and write pages to and from PDFs. You also dove into cropping and rotating pages. Additionally, you’ve learned how to create your own PDF files with the ReportLab package, which has several cool features, including creating pages of different sizes, changing the font, and more.

**In this tutorial, you’ve learned how to:**

- **Read** PDF files and **extract** text using the `pypdf.PdfReader` class
- **Write** new PDF files using the `pypdf.PdfWriter` class
- **Concatenate** and **merge** PDF files using the `pypdf.PdfMerger` class
- **Rotate** and **crop** PDF pages using `pypdf.RectangleObject`
- **Encrypt** and **decrypt** PDF files with passwords
- **Create** and **customize** PDF files from scratch with ReportLab

The ReportLab library is a powerful PDF creation tool. In this tutorial, you only dipped your toe into what’s possible. If you’ve enjoyed this tutorial, then check out the [*Python Basics: A Practical Introduction to Python 3*](https://realpython.com/products/python-basics-book/) book for more.

To review the examples that you just saw, be sure to download the materials by clicking the link below:

## Frequently Asked Questions

Now that you have some experience with creating and modifying PDF files in Python, you can use the questions and answers below to check your understanding and recap what you’ve learned.

These FAQs are related to the most important concepts you’ve covered in this tutorial. Click the *Show/Hide* toggle beside each question to reveal the answer.

You can use the `pypdf` library to read and modify existing PDF files. By using the `PdfReader` class, you can extract text and access page content, while the `PdfWriter` class allows you to write modifications to a new PDF file.

You can create new PDF files from scratch using the ReportLab library. By using the `Canvas` class, you can draw text, set fonts, and define page sizes to generate customized PDF documents.

To encrypt a PDF file, you use the `.encrypt()` method of the `PdfWriter` class, specifying a user password and optionally an owner password. To decrypt, you use the `.decrypt()` method of the `PdfReader` class, providing the correct password.

You can use the `PdfWriter` class from the `pypdf` library to concatenate and merge multiple PDFs. The `.append()` method concatenates PDF files end-to-end, while the `.merge()` method allows you to insert one PDF into another at a specific location.

Yes, Python can create interactive PDFs with forms using the ReportLab library, which allows you to add form elements like text fields and buttons to PDF documents.

🐍 Python Tricks 💌

About **David Amos**

David is a writer, programmer, and mathematician passionate about exploring mathematics through code.

[» More about David](https://realpython.com/team/damos/)

---

*Each tutorial at Real Python is created by a team of developers so that it meets our high quality standards. The team members who worked on this tutorial are:*

Master Real-World Python Skills With Unlimited Access to Real Python

![Locked learning resources](https://realpython.com/static/videos/lesson-locked.f5105cfd26db.svg)

**Join us and get access to thousands of tutorials, hands-on video courses, and a community of expert Pythonistas:**

Master Real-World Python Skills  
With Unlimited Access to Real Python

![Locked learning resources](https://realpython.com/static/videos/lesson-locked.f5105cfd26db.svg)

**Join us and get access to thousands of tutorials, hands-on video courses, and a community of expert Pythonistas:**

Keep Learning

Related Topics: [intermediate](https://realpython.com/tutorials/intermediate/) [tools](https://realpython.com/tutorials/tools/)

Related Tutorials:

- [Reading and Writing WAV Files in Python](https://realpython.com/python-wav-files/?utm_source=realpython&utm_medium=web&utm_campaign=related-post&utm_content=creating-modifying-pdf)
- [Python GUI Programming: Your Tkinter Tutorial](https://realpython.com/python-gui-tkinter/?utm_source=realpython&utm_medium=web&utm_campaign=related-post&utm_content=creating-modifying-pdf)
- [Python's pathlib Module: Taming the File System](https://realpython.com/python-pathlib/?utm_source=realpython&utm_medium=web&utm_campaign=related-post&utm_content=creating-modifying-pdf)
- [Asynchronous Tasks With Django and Celery](https://realpython.com/asynchronous-tasks-with-django-and-celery/?utm_source=realpython&utm_medium=web&utm_campaign=related-post&utm_content=creating-modifying-pdf)
- [Python MarkItDown: Convert Documents Into LLM-Ready Markdown](https://realpython.com/python-markitdown/?utm_source=realpython&utm_medium=web&utm_campaign=related-post&utm_content=creating-modifying-pdf)

![](https://files.realpython.com/media/Python-3s-pathlib-Module-Taming-the-File-System_Watermarked.524352e6d4ce.jpg)

Tutorial

### Python's pathlib Module: Taming the File System

Python's pathlib module enables you to handle file and folder paths in a modern way. This built-in module provides intuitive semantics that work the same way on different operating systems. In this tutorial, you'll get to know pathlib and explore common tasks when interacting with paths.
