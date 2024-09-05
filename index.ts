import type { Adapter } from "@auth/core/adapters"

function request(url: string | URL, method: "POST" | "GET" | "PUT" | "DELETE") {
    return async function <T extends object>(pathname: string, params: T) {
        const uri = new URL(url)

        for (const [name, value] of Object.entries(params)) {
            if (value instanceof Date)
                uri.searchParams.append(name, value.toISOString())

            else if (value)
                uri.searchParams.append(name, value)
        }

        if (!uri.pathname.endsWith("/"))
          uri.pathname += "/"

        uri.pathname += pathname

        const res = await fetch(uri, { method })

        if (res.status !== 200) {
            const { errors } = await res.json()
            throw errors
        }

        return res
    }
}

function date(record: {
    emailVerified?: string,
    expires?: string,
}): any {
    const { emailVerified, expires } = record

    if (emailVerified)
        return { ...record, emailVerified: new Date(emailVerified) }

    if (expires)
        return { ...record, expires: new Date(expires) }

    return record
}

/**
 * Adapter for django-authjs
 *
 * @param url backend server auth endpoint
 * @returns Auth.js adapter
 */
export function DjangoAdapter(url: string | URL): Adapter {
    const get = request(url, "GET")
    const post = request(url, "POST")
    const put = request(url, "PUT")
    const del = request(url, "DELETE")

    return {
        createUser: user => post(`create-user/`, user)
            .then(res => res.json()).then(date)
            .catch(err => {
                console.error("could not create user", err)
            }),

        getUser: userId => get(`get-user/`, { userId })
            .then(res => res.json()).then(date)
            .catch(err => {
                console.error("could not get user", err)
                return null
            }),

        getUserByAccount: acc => get(`get-user-by-email/`, acc)
            .then(res => res.json()).then(date)
            .catch(err => {
                console.error("could not get user by email", err)
                return null
            }),

        updateUser: user => put(`update-user/`, user)
            .then(res => res.json()).then(date)
            .catch(err => {
                console.error("could not update user", err)
                return null
            }),

        linkAccount: account => post(`link-account/`, account)
            .then(res => res.json()).then(date)
            .catch(err => {
                console.error("could not link account", err)
                return null
            }),

        deleteUser: userId => del(`delete-user/`, { userId })
            .then(res => res.json()).then(date)
            .catch(err => {
                console.error("could not delete user", err)
                return null
            }),

        unlinkAccount: acc => del(`unlink-account/`, acc)
            .then(res => res.json()).then(date)
            .catch(err => {
                console.error("could not delete user", err)
                return null
            }),

        createSession: session => post(`create-session/`, session)
            .then(res => res.json()).then(date)
            .catch(err => {
                console.error("could not link account", err)
                return null
            }),

        getSessionAndUser: sessionToken => get(`get-session-and-user/`, { sessionToken })
            .then(res => res.json()).then(({ session, user }) => ({
                session: date(session),
                user: date(user),
            }))
            .catch(err => {
                console.error("could not get session and user", err)
                return null
            }),

        updateSession: session => put(`update-session/`, session)
            .then(res => res.json()).then(date)
            .catch(err => {
                console.error("could not update session", err)
                return null
            }),

        deleteSession: sessionToken => del(`delete-session/`, { sessionToken })
            .then(res => res.json()).then(date)
            .catch(err => {
                console.error("could not update session", err)
                return null
            }),

        getUserByEmail: email => get(`get-user-by-email/`, { email })
            .then(res => res.json()).then(date)
            .catch(err => {
                console.error("could not get user by email", err)
                return null
            }),

        createVerificationToken: token => post(`create-verification-token/`, token)
            .then(res => res.json()).then(date)
            .catch(err => {
                console.error("could not create verification token", err)
                return null
            }),

        useVerificationToken: token => del(`use-verification-token/`, token)
            .then(res => res.json()).then(date)
            .catch(err => {
                console.error("could not use verification token", err)
                return null
            }),
    }
}
