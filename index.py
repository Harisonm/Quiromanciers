import streamlit as st
import pages.userinterface
import pages.biography
import pages.instagram
import pages.about


PAGES = {
    "User Interface": pages.userinterface,
    "Biography Generation": pages.biography,
    "Instagram Classification": pages.instagram,
    "About": pages.about
}


def main():
    page = st.sidebar.radio("Menu", options=list(PAGES.keys()))
    st.title(page)
    PAGES[page].content()


if __name__ == "__main__":
    main()
